# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-16 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180115_1033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(related_name='posts', to='blog.Tag', verbose_name='\u6807\u7b7e'),
        ),
    ]
