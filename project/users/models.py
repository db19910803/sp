from django.db import models

# Create your models here.

# 用户信息表格
class Users(models.Model):
    # 电话
    tel = models.IntegerField()
    # 密码
    password = models.CharField(max_length=32)
    # 头像图片地址
    headjpg = models.CharField(max_length=200,null=True)
    # 昵称
    name = models.CharField(max_length=20,null=True)
    # 性别
    gender = models.IntegerField(choices=((1,'男'),(2,'女'),(0,'保密')),default=0)
    # 出生日期
    birthday = models.DateField(null=True)
    # 就读学校
    school = models.CharField(max_length=200,null=True)
    # 地址
    address = models.CharField(max_length=50,null=True)
    # 故乡
    hometown = models.CharField(max_length=50,null=True)
    # 支付密码
    paypassword = models.CharField(max_length=32,null=True)
    # 账户余额
    balance = models.DecimalField(max_digits=8,decimal_places=2,null=True)
    # 积分
    intgral = models.IntegerField(null=True)
    # 创建时间
    starttime = models.DateTimeField(auto_now_add=True)
    # 更新时间
    updatetime = models.DateTimeField(auto_now=True)
    # 假删除
    delatestate = models.BooleanField(default=False)
    # 红包  多对多的关系,需要建立一个红包列表(由于红包属于商家的,这个表不在users应用里面设计)
    # 收货地址  一对多,需要建立收获地址列表


# 收获地址列表
class Shipaddress(models.Model):
    # 宿舍区
    dormitaryarea = models.CharField(max_length=50)
    # 楼
    tower = models.CharField(max_length=50)
    # 你在哪
    detailarea = models.CharField(max_length=50)
    # 收货人
    person = models.CharField(max_length=20)
    # 联系电话
    linktel = models.IntegerField()
    # 是否设置为默认收获地址
    defaults = models.BooleanField(default=False)
    # 假删除
    delates = models.BooleanField(default=False)
    # 创建时间
    builttime = models.DateTimeField(auto_now_add=True)
    # 修改时间
    changetime = models.DateTimeField(auto_now=True)
    # 外键，用于连接user列表
    linkusers = models.ForeignKey(to='Users')