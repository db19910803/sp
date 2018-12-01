from django.conf.urls import url

from order.views import show, sure_order, pay_ali, success

urlpatterns = [
    url(r"^$",show,name='回显订单首页'),
    url(r"^sure_order/",sure_order,name='订单确认等待支付'),
    url(r"^pay_ali/",pay_ali,name='支付宝支付'),
    url(r"^success/",success,name='支付成功'),
]