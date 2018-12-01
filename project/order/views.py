from django.db import transaction
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render,redirect

# Create your views here.
from goods.models import Goods_SKU
from order.models import new_Transport_style, new_Order_list, new_order_sku_list
from users.models import Users, UserAddress
from users.views import style
from django_redis import get_redis_connection
from alipay import AliPay
import os
from django.conf import settings

@transaction.atomic
@style
def show(request):
    # 当使用的是get方法进行访问的时候,实际上是刷新,此时需要从数据库中查询出对应的数据
    # 查询对应人员的购物车信息,但是这些信息是从购物车中提交过来的
    if request.method == 'GET':
        try:
            sku_id_list = request.GET.get('list_id')
            sku_id_list = sku_id_list.split(',')
        except:
            return redirect('shopping:购物车')
        tel = request.session.get('tel')
        # 从redis中获取对应的sku对象
        cnn = get_redis_connection('default')
        sku_count = [cnn.hget(tel,int(i)) for i in sku_id_list]
        try:
            sku_object = [Goods_SKU.objects.get(pk=int(i)) for i in sku_id_list]
        except:
            # 表明查询错误,则存在sku_id有误,需要进行反馈
            return HttpResponse('商品有误')
        data = [[sku_object[i],sku_count[i]] for i in range(len(sku_id_list))]
        # 查询对应的人是否有地址,如果有则显示默认的地址上去,如果没有则显示添加
        tel = request.session.get('tel')
        try:
            useraddress = Users.objects.get(tel=tel).useraddress_set.filter(delets=False).order_by('-defaults')
        except:
            # 如果没有该用户则报错
            return HttpResponse('用户不存在')
        # 计算出总共的价格并返回
        total_price = sum([float(sku_object[i].price)*float(sku_count[i]) for i in range(len(sku_object))])
        # 从数据库中间直接查询出运输方式,进行网页回显
        trans = new_Transport_style.objects.all()
        constext = {
            'data':data,
            'useraddress':useraddress,
            'total_price':total_price,
            'trans':trans,
        }
        return render(request,'order/tureorder.html',context=constext)
    else:
        # 获取里面的数据
        address_id = request.POST.get('address_id')
        # 获取sku_id
        sku_id = request.POST.getlist('sku_id')
        # 运送方式的id
        send_style = request.POST.get('send_style')
        # 获取对应的用户
        tel = request.session.get('tel')
        # 对输入的数据进行判定
        try:
            address_obj = UserAddress.objects.get(pk=int(address_id))
            order_sku_list=[Goods_SKU.objects.get(pk=int(i)).pk for i in sku_id]
            send_style_obj = new_Transport_style.objects.get(pk=int(send_style))
        except:
            return JsonResponse({'key':1,'msg':'参数错误'})
        # 需要写对应的表单数据
        # 获取对应的order对象
        sid = transaction.savepoint()
        order = new_Order_list.objects.create(
            # 进行数据的写入
            # 关联用户
            user_id_id = Users.objects.get(tel=tel).pk,
            # 收货人
            get_person = address_obj.person,
            # 收货人电话
            get_person_tel = address_obj.linktel,
            # 订单地址
            order_address = address_obj.hcity+address_obj.hproper+address_obj.harea+address_obj.detail,
            # 运输方式 外键
            transport_id = send_style_obj.pk,
            # 付款方式
            pay_id = 1,
        )
        # 先不保存,最后再保存
        # 存储new_order_sku_list列表,将里面的sku进行对应
        # 对应的购买数量的数据需要从redis中取出
        cnn = get_redis_connection('default')
        sku_count_list = [int(cnn.hget(str(tel),str(i))) for i in order_sku_list]
        # 针对已经选中的商品进行是否库存充足的判断
        # 取出对应商品的库存
        sku_stock_list = [int(Goods_SKU.objects.get(pk=i).stock) for i in order_sku_list]
        # 进行判定
        for i in range(len(sku_count_list)):
            if sku_count_list[i] >= sku_stock_list[i]:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'key':3, 'msg':'有商品库存不足'})

        # 存储对应的数据
        # 真实物品总金额
        goods_total_price = 0
        try:
            for i in range(len(order_sku_list)):
                new_order_sku_list_obj= new_order_sku_list.objects.create(goods_sku_id=order_sku_list[i],
                                                  link_order_list_id=order.pk,
                                                  sku_count=sku_count_list[i],
                                                  sku_price=Goods_SKU.objects.get(pk=order_sku_list[i]).price,
                                                  )
                # 进行总价计算
                goods_total_price += new_order_sku_list_obj.sku_price*new_order_sku_list_obj.sku_count
                new_order_sku_list_obj.save()
            # 计算加上运费的总价格
            order_price = goods_total_price+send_style_obj.price
        except:
            transaction.savepoint_rollback(sid)
            return JsonResponse({'key':2,'msg':'数据写入有错'})
        # 继续对new_Order_list进行写入,将计算的两个价格进行写入
        order.order_price = order_price
        order.goods_total_price = goods_total_price
        order_id = order.pk
        # 最后保存order列表
        order.save()
        # 保存成功后需要对sku的库存和销量进行修改
        for i in range(len(order_sku_list)):
            # 进行修改
            Goods_SKU.objects.get(pk=order_sku_list[i]).sales += sku_count_list[i]
            Goods_SKU.objects.get(pk=order_sku_list[i]).stock -= sku_count_list[i]
        # 之后删除redis中的数据
        cnn.hdel(tel,*order_sku_list)
        # 最后将order_id返回出去
        transaction.savepoint_commit(sid)

        return JsonResponse({'key':0,'msg':'成功','order':order_id})


# 确认订单并支付
@style
def sure_order(request):
    if request.method == 'GET':
        # 获取对应的orderid
        tel = request.session.get('tel')
        try:
            order_obj = new_Order_list.objects.get(pk=request.GET.get('order_id'),user_id=Users.objects.get(tel=tel).pk)
        except:
            return redirect('shopping:购物车')
        context = {
            'data':order_obj,
        }
        return render(request,'order/order.html',context=context)
    else:
        pass


# 支付宝付款页面
def pay_ali(request):
    app_private_key_string = open(os.path.join(settings.BASE_DIR,'order/private_key.pem')).read()
    alipay_public_key_string = open(os.path.join(settings.BASE_DIR,'order/public_key.pem')).read()

    # 调节并实例化
    alipay = AliPay(
        appid="2016092300577216",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=app_private_key_string,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=alipay_public_key_string,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug = True  # 默认False
    )
    # 从数据库中获取对应的订单id以及查询出订单的信息
    try:
        user_id = Users.objects.get(tel=request.session.get('tel')).pk
        order_id = request.GET.get('order_id')
        order = new_Order_list.objects.get(pk=order_id,user_id=user_id)
    except:
        return HttpResponse('乱求输入')

    order_string = alipay.api_alipay_trade_wap_pay(
        out_trade_no="{}".format(order.order_list_number), # 订单号
        total_amount=str(order.goods_total_price), # 金额
        subject='商品订单详情',
        return_url="http://127.0.0.1:8000/order/success", # 这里是成功后跳转的
        notify_url=None  # 可选, 不填则使用默认notify url
    )
    # 成功后进行跳转
    return redirect('https://openapi.alipaydev.com/gateway.do?{}'.format(order_string))

# 支付成功后的页面
def success(request):
    return HttpResponse('对的')