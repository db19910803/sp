# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-23 14:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Public_form',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('add_time', models.DateTimeField(auto_now_add=True)),
                ('change_time', models.DateTimeField(auto_now=True)),
                ('deletes', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Active_goods',
            fields=[
                ('public_form_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='goods.Public_form')),
            ],
            bases=('goods.public_form',),
        ),
        migrations.CreateModel(
            name='Goods_class',
            fields=[
                ('public_form_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='goods.Public_form')),
                ('name', models.CharField(max_length=20, verbose_name='分类名')),
                ('short_information', models.TextField(verbose_name='分类简介')),
            ],
            bases=('goods.public_form',),
        ),
        migrations.CreateModel(
            name='Goods_jpg',
            fields=[
                ('public_form_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='goods.Public_form')),
                ('address', models.CharField(max_length=200, verbose_name='图片地址')),
            ],
            bases=('goods.public_form',),
        ),
        migrations.CreateModel(
            name='Goods_SKU',
            fields=[
                ('public_form_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='goods.Public_form')),
                ('name', models.CharField(max_length=20, verbose_name='商品名称')),
                ('short_information', models.TextField(verbose_name='简介')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='价格')),
                ('stock', models.IntegerField(verbose_name='库存')),
                ('sales', models.IntegerField(verbose_name='销量')),
                ('logo_address', models.CharField(max_length=200, verbose_name='Logo地址')),
                ('put_away', models.BooleanField(default=False, verbose_name='上架')),
                ('goods_class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods_class')),
            ],
            bases=('goods.public_form',),
        ),
        migrations.CreateModel(
            name='Goods_SUP',
            fields=[
                ('public_form_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='goods.Public_form')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('detail', models.TextField(verbose_name='详情')),
            ],
            bases=('goods.public_form',),
        ),
        migrations.CreateModel(
            name='Index_active_area',
            fields=[
                ('public_form_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='goods.Public_form')),
                ('name', models.CharField(max_length=20, verbose_name='活动专区名称')),
                ('description', models.TextField(verbose_name='活动描述')),
                ('order', models.SmallIntegerField(default=0, verbose_name='活动排序')),
                ('put_away', models.BooleanField(default=False, verbose_name='上架')),
            ],
            bases=('goods.public_form',),
        ),
        migrations.CreateModel(
            name='Index_active_list',
            fields=[
                ('public_form_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='goods.Public_form')),
                ('name', models.CharField(max_length=20, verbose_name='活动名称')),
                ('active_jpg_address', models.CharField(max_length=200, verbose_name='活动展示图片地址')),
                ('link_url', models.CharField(max_length=200, verbose_name='活动链接地址')),
            ],
            bases=('goods.public_form',),
        ),
        migrations.CreateModel(
            name='Index_run_jpg',
            fields=[
                ('public_form_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='goods.Public_form')),
                ('name', models.CharField(max_length=50)),
                ('jpg_address', models.CharField(max_length=200)),
                ('order', models.SmallIntegerField(default=0)),
                ('to_goods_sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods_SKU')),
            ],
            bases=('goods.public_form',),
        ),
        migrations.AddField(
            model_name='goods_sku',
            name='goods_spu_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods_SUP'),
        ),
        migrations.AddField(
            model_name='goods_jpg',
            name='goods_sku_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods_SKU', verbose_name='对应商品'),
        ),
        migrations.AddField(
            model_name='active_goods',
            name='link_SKU',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Goods_SKU', verbose_name='连接的商品'),
        ),
        migrations.AddField(
            model_name='active_goods',
            name='link_active_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.Index_active_area', verbose_name='连接的活动区域'),
        ),
    ]
