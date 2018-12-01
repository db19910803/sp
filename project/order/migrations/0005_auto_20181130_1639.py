# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-30 16:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_auto_20181130_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='new_order_list',
            name='goods_total_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='真是总金额'),
        ),
        migrations.AlterField(
            model_name='new_order_list',
            name='order_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='总金额'),
        ),
    ]
