from django.contrib import admin

# Register your models here.
from goods.models import Index_run_jpg, Goods_SKU, Goods_class, Goods_SUP, Goods_jpg, Index_active_list, \
    Index_active_area, Active_goods

# admin.site.register(Index_run_jpg)
@admin.register(Index_run_jpg)
class Index_run_jpgAdmin(admin.ModelAdmin):
    list_display = ('id','name','jpg_address','order','to_goods_sku')
    list_editable = ['jpg_address','order','to_goods_sku']
    list_filter = ('order',)
    # 字段为空的时候现实的内容
    empty_value_display = '-空-'

@admin.register(Goods_SKU)
class Goods_SKUAdmin(admin.ModelAdmin):
    list_display = ('id','name','short_information','price','stock','sales','show_logo','put_away','change_time','deletes')
    list_editable = ['price','stock','sales','put_away','deletes']
    list_filter = ('price','stock','sales','put_away')

@admin.register(Goods_class)
class Goods_classAdmin(admin.ModelAdmin):
    list_display = ('id','name','short_information')
    list_editable = ['short_information']

@admin.register(Goods_SUP)
class Goods_SUPAdmin(admin.ModelAdmin):
    list_display = ('id','name','detail')
    list_editable = ['detail']

@admin.register(Goods_jpg)
class Goods_jpgAdmin(admin.ModelAdmin):
    list_display = ('id','address','goods_sku_id')
    list_editable = ['address','goods_sku_id']

@admin.register(Index_active_list)
class Index_active_listAdmin(admin.ModelAdmin):
    list_display = ('id','name','active_jpg_address','link_url')
    list_editable = ['active_jpg_address','link_url']

@admin.register(Index_active_area)
class Index_active_areaAdmin(admin.ModelAdmin):
    list_display = ('id','name','description','order','put_away')
    list_editable = ['description','order','put_away']
    list_filter = ('order','put_away')

@admin.register(Active_goods)
class Active_goodsAdmin(admin.ModelAdmin):
    list_display = ('link_active_area','link_SKU')


# 关联添加,针对的是活动专区Index_active_area与活动产品Active_goods进行组合添加方式
# class tegatherAdminInline(admin.TabularInline):
#     model = Active_goods
#     extra = 2
#
# @admin.register(Index_active_area)
# class Index_active_areaAdmin(admin.ModelAdmin):
#     list_display = ('id','name','description','order','put_away')
    # list_editable = ['description','order','put_away']
    # list_filter = ('order','put_away')
    # inlines = [
    #     tegatherAdminInline
    # ]