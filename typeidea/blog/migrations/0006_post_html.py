# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-19 07:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_is_markdown'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='html',
            field=models.TextField(default='', help_text='\u76ee\u524d\u652f\u6301Markdown\u683c\u5f0f', verbose_name='\u6e32\u67d3\u540e\u7684\u6570\u636e'),
        ),
    ]