from django.conf.urls import url

from shopping.views import show

urlpatterns = [
    url(r'^$',show)
]