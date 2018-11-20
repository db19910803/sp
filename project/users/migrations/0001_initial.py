# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 11:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Shipaddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dormitaryarea', models.CharField(max_length=50)),
                ('tower', models.CharField(max_length=50)),
                ('detailarea', models.CharField(max_length=50)),
                ('person', models.CharField(max_length=20)),
                ('linktel', models.IntegerField()),
                ('defaults', models.BooleanField(default=False)),
                ('delates', models.BooleanField(default=False)),
                ('builttime', models.DateField(auto_now_add=True)),
                ('changetime', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.IntegerField()),
                ('password', models.CharField(max_length=32)),
                ('headjpg', models.CharField(max_length=200, null=True)),
                ('name', models.CharField(max_length=20, null=True)),
                ('gender', models.IntegerField(choices=[(1, '男'), (2, '女'), (0, '保密')], default=0)),
                ('birthday', models.DateField(null=True)),
                ('school', models.CharField(max_length=200, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('hometown', models.CharField(max_length=50, null=True)),
                ('paypassword', models.CharField(max_length=32, null=True)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('intgral', models.IntegerField(null=True)),
                ('starttime', models.DateField(auto_now_add=True)),
                ('updatetime', models.DateField(auto_now=True)),
                ('delatestate', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='shipaddress',
            name='linkusers',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Users'),
        ),
    ]
