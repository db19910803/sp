from django.conf.urls import url

from users.views import show, log_in, reg_in, findback

urlpatterns = [
    url(r'^$',show,name='个人主页'),
    url(r'^reg_in/$',reg_in,name='注册'),
    url(r'^log_in/$',log_in,name='登录'),
    url(r'^findback/$',findback,name='找回密码'),
]