from django.db import models

class Public_form(models.Model):
    add_time = models.DateTimeField(auto_now_add=True) # 公共的添加时间
    change_time = models.DateTimeField(auto_now=True,verbose_name='更新时间') # 修改时间
    deletes = models.BooleanField(default=False,verbose_name='是否删除') # 假删除