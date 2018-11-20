from django.conf.urls import url

from order.views import show

urlpatterns = [
    url(r"^$",show)
]