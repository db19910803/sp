from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django_redis import get_redis_connection

# Create your views here.
from django.views import View

from goods.models import Goods_SKU
from users.views import style


def show(request):
    return HttpResponse('ok')


class go_shopping(View):
    def get(self,request):
        pass

    def post(self,request):
        # 从页面获取数据,需要从页面获取对应的sku_id,购买数量count,从session中获得用户tel
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')
        # 拿到数据后对数据进行验证,用户tel是从个session中拿的,判定是否存在
        # sku_id要判定是否是数字,count需要判定是否是数字
        # 如果数据没有问题才进行数据库的写入,如果有问题则返回错误信息
        if not request.session.get('tel'):
            return JsonResponse({'key':1,'errormsg':'用户没有登录'})
        else:
            tel = request.session.get('tel')
        try:
            sku_id = int(sku_id)
            # 针对商品ID进行判断商品是否存在
            Goods_SKU.objects.get(pk=sku_id)
        except:
            return JsonResponse({'key':2,'errormsg':'商品ID不合法'})
        try:
            count = int(count)
            # 进行判定是否已经超出了库存
            num = Goods_SKU.objects.get(pk=sku_id).sales
            if count >= int(num):
                return JsonResponse({'key':4,'errormsg':'商品数目不合法'})
        except:
            return JsonResponse({'key':3,'errormsg':'商品数目不合法'})
        # 数据都验证通过,则需要进行数据库的写入,这里写入的是redis数据库
        # 创建redis连接
        cnn = get_redis_connection('default')
        # 进行数据写入
        res = cnn.hincrby(tel,sku_id,count)
        # 如果数据库中的商品数量已经到0,则需要删除该sku_id
        if res == 0:
            # 进行数据库删除
            cnn.hdel(tel,sku_id)
        # 数据写入完成后则进行返回
        return JsonResponse({'key':0,'errormsg':'写入数据库成功'})

# 购物车
@style  # 进行登录判断
def shopping_car(request):
    if request.method == 'GET':
        # 进行数据库里拿出对应的sku_id,count
        tel = request.session.get('tel')
        # 进行数据库查询
        cnn = get_redis_connection('default')
        res = cnn.hgetall(tel)
        # 针对查询的字典进行遍历改写
        goods_list = []
        for k,v in res.items():
            sku_id, count = int(k),int(v)
            goods = Goods_SKU.objects.get(pk=sku_id)
            goods.count = count
            goods_list.append(goods)
        # 构造数据进行传入
        context = {
            'goods_list':goods_list,
        }
        return render(request,'shopping/shopcart.html',context=context)
    else:
        pass