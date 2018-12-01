from django.db import models

# Create your models here.

# 订单信息列表
from goods.helper_to_goods.modle_to_public import Public_form


class new_Order_list(models.Model):
    order_list_number = models.IntegerField(auto_created=True,blank=True,null=True,verbose_name='订单编号')
    order_price = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='总金额')
    rel_order_price = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='真实付款总金额')
    goods_total_price = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='真实物品总金额')
    # 关联用户列表
    user_id = models.ForeignKey(to='users.Users',verbose_name='用户的id')
    get_person = models.CharField(max_length=20,verbose_name='收货人')
    get_person_tel = models.CharField(max_length=11,verbose_name='收货人电话')
    order_address = models.CharField(max_length=200,verbose_name='订单地址')
    order_status = models.IntegerField(default=0,choices=((0,'待付款'),(1,'退发货'),(2,'待收货'),(3,'待评价'),(4,'已完成')))
    # 运输方式 多对一 transport为一
    transport = models.ForeignKey(to='new_Transport_style',verbose_name='运输方式')
    # 付款方式 多对一 pay_style为一
    pay = models.ForeignKey(to='new_Pay_style',verbose_name='支付方式')

    add_time = models.DateTimeField(auto_now_add=True)  # 公共的添加时间
    change_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 修改时间
    deletes = models.BooleanField(default=False, verbose_name='是否删除')  # 假删除


class new_Transport_style(models.Model):
    name = models.CharField(max_length=50,verbose_name='运输方式名称')
    price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='运输单价')
    add_time = models.DateTimeField(auto_now_add=True)  # 公共的添加时间
    change_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 修改时间
    deletes = models.BooleanField(default=False, verbose_name='是否删除')  # 假删除

    class Meta:
        verbose_name = '运输方式表'
        verbose_name_plural = verbose_name

class new_Pay_style(models.Model):
    name = models.CharField(max_length=50,verbose_name='支付方式名称')
    pay_img = models.ImageField(upload_to='order/index/%Y%m%d',verbose_name='支付图片')
    add_time = models.DateTimeField(auto_now_add=True)  # 公共的添加时间
    change_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 修改时间
    deletes = models.BooleanField(default=False, verbose_name='是否删除')  # 假删除


class new_order_sku_list(models.Model):
    goods_sku = models.ForeignKey(to='goods.Goods_SKU',verbose_name='连接sku')
    link_order_list = models.ForeignKey(to='new_Order_list',verbose_name='连接订单详情')
    sku_count = models.IntegerField(verbose_name='订单数量')
    sku_price = models.DecimalField(max_digits=10,decimal_places=2,verbose_name='sku_单价')

    add_time = models.DateTimeField(auto_now_add=True)  # 公共的添加时间
    change_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 修改时间
    deletes = models.BooleanField(default=False, verbose_name='是否删除')  # 假删除
