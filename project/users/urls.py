from django.conf.urls import url

from users.views import show, log_in, reg_in, findback, personpage, gladdress, address, short_msg, choice_address, \
    address_change, address_delet, set_default

urlpatterns = [
    url(r'^$',show,name='主页'),
    url(r'^reg_in/$',reg_in,name='注册'),
    url(r'^log_in/$',log_in,name='登录'),
    url(r'^findback/$',findback,name='找回密码'),
    url(r'^infor/$',personpage,name='个人首页'),
    url(r'^gladdress/$',gladdress,name='收货地址显示页'),
    url(r'^address/$',address,name='添加'),
    url(r'^short_msg/$',short_msg,name='短信验证'),
    url(r'^choice_address/$',choice_address,name='添加收货地址'),
    url(r'^address_change/',address_change,name='修改收货地址'),
    url(r'^address_delet/',address_delet,name='删除收货地址'),
    url(r'^set_default/',set_default,name='修改默认地址'),
]