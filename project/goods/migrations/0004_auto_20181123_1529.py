# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-23 15:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_auto_20181123_1502'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='active_goods',
            options={'verbose_name': '活动专区展示商品表', 'verbose_name_plural': '活动专区展示商品表'},
        ),
        migrations.AlterModelOptions(
            name='goods_class',
            options={'verbose_name': '分类页面分类表', 'verbose_name_plural': '分类页面分类表'},
        ),
        migrations.AlterModelOptions(
            name='goods_jpg',
            options={'verbose_name': '商品详细页面轮播图', 'verbose_name_plural': '商品详细页面轮播图'},
        ),
        migrations.AlterModelOptions(
            name='goods_sku',
            options={'verbose_name': '商品详细参数表', 'verbose_name_plural': '商品详细参数表'},
        ),
        migrations.AlterModelOptions(
            name='goods_sup',
            options={'verbose_name': '商品类别表', 'verbose_name_plural': '商品类别表'},
        ),
        migrations.AlterModelOptions(
            name='index_active_area',
            options={'verbose_name': '首页专区名称表', 'verbose_name_plural': '首页专区名称表'},
        ),
        migrations.AlterModelOptions(
            name='index_active_list',
            options={'verbose_name': '首页推荐活动表', 'verbose_name_plural': '首页推荐活动表'},
        ),
        migrations.AlterModelOptions(
            name='index_run_jpg',
            options={'verbose_name': '首页商品轮播图', 'verbose_name_plural': '首页商品轮播图'},
        ),
        migrations.AlterField(
            model_name='goods_jpg',
            name='address',
            field=models.ImageField(upload_to='goods/商品SKU详情页/%Y%m%d', verbose_name='图片地址'),
        ),
        migrations.AlterField(
            model_name='goods_sku',
            name='logo_address',
            field=models.ImageField(upload_to='goods/商品SKU/%Y%m%d', verbose_name='Logo地址'),
        ),
        migrations.AlterField(
            model_name='index_active_list',
            name='active_jpg_address',
            field=models.ImageField(upload_to='goods/活动展示/%Y%m%d', verbose_name='活动展示图片地址'),
        ),
        migrations.AlterField(
            model_name='index_run_jpg',
            name='jpg_address',
            field=models.ImageField(upload_to='goods/首页/%Y%m%d', verbose_name='图片连接地址'),
        ),
    ]
