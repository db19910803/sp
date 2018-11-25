from django.conf.urls import url

from goods.views import show, goods_detail, category_show

urlpatterns = [
    url(r'^$',show),
    url(r'^goods_detail/(?P<id>\d+).html$',goods_detail,name='商品详情'),
    url(r'^category/(?P<goods_id>\d+)/(?P<order_id>\d+)/$',category_show,name='分类页'),
]