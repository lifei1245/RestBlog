# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-01-25 11:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20180125_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='add_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime.now, null=True, verbose_name='添加时间'),
        ),
    ]
