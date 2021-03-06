# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-23 15:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0004_auto_20181123_1529'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods_jpg',
            name='address',
            field=models.ImageField(upload_to='goods/goodsSKUdetail/%Y%m%d', verbose_name='图片地址'),
        ),
        migrations.AlterField(
            model_name='goods_sku',
            name='logo_address',
            field=models.ImageField(upload_to='goods/goodsSKU/%Y%m%d', verbose_name='Logo地址'),
        ),
        migrations.AlterField(
            model_name='index_active_list',
            name='active_jpg_address',
            field=models.ImageField(upload_to='goods/activeShow/%Y%m%d', verbose_name='活动展示图片地址'),
        ),
        migrations.AlterField(
            model_name='index_run_jpg',
            name='jpg_address',
            field=models.ImageField(upload_to='goods/index/%Y%m%d', verbose_name='图片连接地址'),
        ),
    ]
