from django.db import models
from django.conf import  settings
# Create your models here.

# 创建首页的轮播图数据列表
from goods.helper_to_goods.modle_to_public import Public_form


class Index_run_jpg(Public_form):
    name = models.CharField(max_length=50,verbose_name='名称') # 名称
    jpg_address = models.ImageField(upload_to='goods/index/%Y%m%d',verbose_name='图片连接地址') # 图片连接地址
    order = models.SmallIntegerField(default=0,verbose_name='优先级') # 排序
    # 下面是进行对外连接的,一个商品可以对应多个轮播,这里需要商品具体的SKUID
    to_goods_sku = models.ForeignKey(to='Goods_SKU',verbose_name='具体商品连接')
    def __str__(self):
        return '首页轮播图片'
    class Meta:
        verbose_name = '首页商品轮播图'
        verbose_name_plural = verbose_name

# 商品的SKU表格
class Goods_SKU(Public_form):
    name = models.CharField(max_length=20,verbose_name='商品名称') # 商品名称
    short_information = models.TextField(verbose_name='简介') # 商品简介
    price = models.DecimalField(max_digits=8,decimal_places=2,verbose_name='价格')
    stock = models.IntegerField(verbose_name='库存')
    sales = models.IntegerField(verbose_name='销量')
    logo_address = models.ImageField(upload_to='goods/goodsSKU/%Y%m%d',verbose_name='Logo地址')
    # 进行logo显示
    def show_logo(self):
        return '<img src="{}{}" style="width: 80px;" alt="">'.format(settings.MEDIA_URL,self.logo_address)
    # 取消页面对标签的转义
    show_logo.allow_tags = True
    show_logo.short_description = '商标图'

    put_away = models.BooleanField(default=False,verbose_name='上架')
    goods_class_id = models.ForeignKey(to='Goods_class') # 商品的分类ID,需要连接商品分类表
    goods_spu_id = models.ForeignKey(to='Goods_SUP') # 商品的SPU表格
    class Meta:
        verbose_name = '商品详细参数表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# 产品分类列表(该表是写在对应的商品分类页面中)
class Goods_class(Public_form):
    name = models.CharField(max_length=20,verbose_name='分类名')
    short_information = models.TextField(verbose_name='分类简介')
    class Meta:
        verbose_name = '分类页面分类表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# 商品SUP列表
class Goods_SUP(Public_form):
    name = models.CharField(max_length=20,verbose_name='名称')
    detail = models.TextField(verbose_name='详情')
    class Meta:
        verbose_name = '商品类别表'
        verbose_name_plural = verbose_name
    def __str__(self):
        return self.name

# 商品的具体图片信息列表,与SKU中的id呈现多对一得关系
class Goods_jpg(Public_form):
    address = models.ImageField(upload_to='goods/goodsSKUdetail/%Y%m%d',verbose_name='图片地址')
    goods_sku_id = models.ForeignKey(to='Goods_SKU',verbose_name='对应商品')
    def __str__(self):
        return '商品详情图片'

    class Meta:
        verbose_name = '商品详细页面轮播图'
        verbose_name_plural = verbose_name

# 商品首页的活动列表名列表
class Index_active_list(Public_form):
    name = models.CharField(max_length=20,verbose_name='活动名称')
    active_jpg_address = models.ImageField(upload_to='goods/activeShow/%Y%m%d',verbose_name='活动展示图片地址')
    link_url = models.CharField(max_length=200,verbose_name='活动链接地址')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '首页推荐活动表'
        verbose_name_plural = verbose_name

# 活动专区列表
class Index_active_area(Public_form):
    name = models.CharField(max_length=20,verbose_name='活动专区名称')
    description = models.TextField(verbose_name='活动描述')
    order = models.SmallIntegerField(default=0,verbose_name='活动排序')
    put_away = models.BooleanField(default=False,verbose_name='上架')
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '首页专区名称表'
        verbose_name_plural = verbose_name

# 活动专区的商品展示,展示商品与活动专区列表呈现的是多对一的关系
class Active_goods(Public_form):
    link_active_area = models.ForeignKey(to='Index_active_area',verbose_name='连接的活动区域')
    link_SKU = models.ForeignKey(to='Goods_SKU',verbose_name='连接的商品')
    def __str__(self):
        return '活动专区展示商品'
    class Meta:
        verbose_name = '活动专区展示商品表'
        verbose_name_plural = verbose_name