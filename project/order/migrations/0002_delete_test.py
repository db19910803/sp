# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-19 08:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Test',
        ),
    ]