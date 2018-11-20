# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-20 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20181119_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='balance',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='gender',
            field=models.IntegerField(choices=[(1, '男'), (2, '女')], default=1),
        ),
        migrations.AlterField(
            model_name='users',
            name='headjpg',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='hometown',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='intgral',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='paypassword',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='school',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]