from django.contrib import admin

# Register your models here.
from order.models import new_Transport_style, new_Pay_style


@admin.register(new_Transport_style)
class new_Transport_styleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')



@admin.register(new_Pay_style)
class new_Pay_styleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')