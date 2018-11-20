from django.conf.urls import url

from goods.views import show

urlpatterns = [
    url(r'^$',show)
]