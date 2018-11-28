from django.db import models

# Create your models here.

# 订单信息列表
from goods.helper_to_goods.modle_to_public import Public_form


class Order_list(Public_form):
    order_list_number = models.IntegerField(auto_created=True,blank=True,null=True,verbose_name='订单编号')
    order_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='总金额')
    # 关联用户列表
    user_id = models.ForeignKey(to='users.Users',verbose_name='用户的id')
    get_person = models.CharField(max_length=20,verbose_name='收货人')
    get_person_tel = models.IntegerField(verbose_name='收货人电话')
    order_address = models.CharField(max_length=200,verbose_name='订单地址')
    order_status = models.IntegerField(choices=((0,'代付款'),(1,'退发货'),(2,'待收货'),(3,'待评价'),(4,'已完成')))
    # 运输方式 多对一 transport为一
    transport = models.ForeignKey(to='Transport_style',verbose_name='运输方式')
    # 付款方式 多对一 pay_style为一
    pay = models.ForeignKey(to='Pay_style',verbose_name='支付方式')
    rel_pay_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='实付款')

# 运输方式表
class Transport_style(Public_form):
    name = models.CharField(max_length=50,verbose_name='运输方式名称')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='运输单价')

# 支付方式表
class Pay_style(Public_form):
    name = models.CharField(max_length=50,verbose_name='支付方式名称')
    pay_img = models.ImageField(upload_to='order/index/%Y%m%d',verbose_name='商标图连接')

# 订单商品表
class Order_sku_list(Public_form):
    # goods_sku_id = models.ForeignKey(to='goods.Goods_SKU',verbose_name='商品的SKU-ID')
    goods_count = models.IntegerField(verbose_name='商品数量')
    goods_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='商品单价')
    # 订单表以多对一的方式进行连接订单列表
    link_to_order_list = models.ForeignKey(to='Order_list',verbose_name='连接订单表ID')



