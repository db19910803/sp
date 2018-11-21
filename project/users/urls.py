from django.conf.urls import url

from users.views import show, log_in, reg_in, findback, personpage, gladdress, address, short_msg

urlpatterns = [
    url(r'^$',show,name='主页'),
    url(r'^reg_in/$',reg_in,name='注册'),
    url(r'^log_in/$',log_in,name='登录'),
    url(r'^findback/$',findback,name='找回密码'),
    url(r'^infor/$',personpage,name='个人首页'),
    url(r'^gladdress/$',gladdress,name='收货地址显示页'),
    url(r'^address/$',address,name='添加收货地址'),
    url(r'^short_msg/$',short_msg,name='短信验证'),
]