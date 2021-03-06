from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection

from goods.models import Index_run_jpg, Index_active_list, Index_active_area, Goods_SKU, Goods_class


def show(request):
    # 显示轮播的图片,从数据库中进行查取并显示到页面
    run_jpg = Index_run_jpg.objects.get(pk=6).jpg_address
    # 查询出对应
    active_jpg = Index_active_list.objects.all().order_by('pk')[:6]
    # 专区列表查询并查询出对应的商品
    # 查询出.首页专区的名称列表
    active_area = Index_active_area.objects.all()
    # 因为是个查询集合,所以需要进行遍历进一步查询
    # data = {}
    # for i in active_area:
    #     data['{}'.format(i.name)] = ''
    #     for j in i.active_goods_set.all():
    #         j.link_SKU.all()
    first_pk = Goods_class.objects.first().pk
    context = {
        'jpg':run_jpg,
        'active_jpg':active_jpg,
        'active_area':active_area,
        'first_pk':first_pk,
    }
    return render(request,'goods/index.html',context=context)

# 商品详情页面显示功能
def goods_detail(request,id):
    # 从页面上获得对应的id
    # 针对上面的轮播进行查询,先根据ID找到对应的sku
    try:
        data = Goods_SKU.objects.get(pk=id)
        # 如果查询到的id存在则需要进行针对页面进行渲染
        # spu的查询是sku的多对一得方式,轮播图的查询是sku的一对多方式
        context = {
            'data':data
        }
        return render(request,'goods/detail.html',context=context)
    except Goods_SKU.DoesNotExist:
        return render(request,'goods/index.html')

# 分类页面
def category_show(request,goods_id,order_id):
    # 查询出对应的分类列表进行显示
    goods_class = Goods_class.objects.all()
    # 根据分类页面的对应pk查询出分类页面的商品
    # 针对上方的点击事件,进行排序的预处理
    order_rul = ['pk', '-sales', '-price', 'price', '-add_time']
    try:
        order_id = int(order_id)
        goods = Goods_class.objects.get(pk=goods_id).goods_sku_set.all().order_by(order_rul[order_id])
    except:
        order_id = 0
        goods = Goods_class.objects.first().goods_sku_set.all().order_by(order_rul[order_id])
    # 进行分页的操作
    page_size = 10
    p = Paginator(goods,page_size)
    # 从页面获得对应的数据,如果没有则显示第一页
    get_page = request.GET.get('page_id', 1)
    # 对获得的数据进行进行判断,如果超过总页数,则显示最后一页,如果小于第一页则显示第一页
    try:
        content = p.page(get_page) # 如果不是整数会报p错
    except PageNotAnInteger:
        content = p.page(1)
    except EmptyPage:
        content = p.page(p.num_pages) # 如果超过总页数则显示最后一页
    goods = content # 将显示结果重新赋值给goods
    context = {
        'goods_class':goods_class,
        'goods_id':int(goods_id),
        'order':order_id,
        'goods':goods,
    }
    return  render(request,'goods/category.html',context=context)

# 进行购物添加的方式
def ajax_add_goods(request):
    # 必须进行验证用户
    if request.method == 'POST':
        # 从页面获取数据,需要从页面获取对应的sku_id,购买数量count,从session中获得用户tel
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 拿到数据后对数据进行验证,用户tel是从个session中拿的,判定是否存在
        # sku_id要判定是否是数字,count需要判定是否是数字
        # 如果数据没有问题才进行数据库的写入,如果有问题则返回错误信息
        if not request.session.get('tel'):
            return JsonResponse({'key': 1, 'errormsg': '用户没有登录'})
        else:
            tel = request.session.get('tel')
        try:
            sku_id = int(sku_id)
            # 针对商品ID进行判断商品是否存在
            Goods_SKU.objects.get(pk=sku_id)
        except:
            return JsonResponse({'key': 2, 'errormsg': '商品ID不合法'})
        try:
            count = int(count)
            # 进行判定是否已经超出了库存
            num = Goods_SKU.objects.get(pk=sku_id).sales
            if count >= int(num):
                return JsonResponse({'key': 4, 'errormsg': '商品数目不合法'})
        except:
            return JsonResponse({'key': 3, 'errormsg': '商品数目不合法'})
        # 数据都验证通过,则需要进行数据库的写入,这里写入的是redis数据库
        # 创建redis连接
        cnn = get_redis_connection('default')
        # 进行数据写入
        res = cnn.hincrby(tel, sku_id, count)
        # 这里需要进行判断
        if res == 0:
            # 表示已经减少到了零,需要从数据库中间删除对应的filed
            cnn.hdel(tel, sku_id)
        # 数据写入完成后则进行返回,并且需要返回整个数据库中所有商品的总和
        # 查询数据库,得到总和
        nums = cnn.hgetall(tel)
        sum = 0
        for k,v in nums.items():
            sum += int(v.decode('utf-8'))
        return JsonResponse({'key': 0, 'errormsg': '写入数据库成功','sum':sum})
    else:
        pass