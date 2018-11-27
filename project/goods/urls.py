from django.conf.urls import url

from goods.views import show, goods_detail, category_show, ajax_add_goods

urlpatterns = [
    url(r'^$',show,name='index'),
    url(r'^goods_detail/(?P<id>\d+).html$',goods_detail,name='商品详情'),
    url(r'^category/(?P<goods_id>\d+)/(?P<order_id>\d+)/$',category_show,name='分类页'),
    url(r'^ajax_add_goods$',ajax_add_goods,name='产品分类列表ajax添加'),
]