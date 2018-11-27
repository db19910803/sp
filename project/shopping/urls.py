from django.conf.urls import url

from shopping.views import show, go_shopping, shopping_car

urlpatterns = [
    url(r'^$',shopping_car,name='购物车'),
    url(r'^go_shopping/$',go_shopping.as_view(),name='ajax购物功能'),
]