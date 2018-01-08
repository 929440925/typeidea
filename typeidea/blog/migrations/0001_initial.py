# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-01-08 08:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('status', models.PositiveIntegerField(choices=[(1, '\u6b63\u5e38'), (2, '\u5220\u9664')], default=1, verbose_name='\u72b6\u6001')),
                ('is_nav', models.BooleanField(default=False, verbose_name='\u662f\u5426\u4e3a\u5bfc\u822a')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u4f5c\u8005')),
            ],
            options={
                'verbose_name': '\u5206\u7c7b',
                'verbose_name_plural': '\u5206\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='\u6807\u9898')),
                ('desc', models.CharField(blank=True, max_length=1024, verbose_name='\u6458\u8981')),
                ('content', models.TextField(help_text='\u6b63\u6587\u5fc5\u987b\u4e3aMarkDown\u683c\u5f0f', verbose_name='\u6b63\u6587')),
                ('status', models.PositiveIntegerField(choices=[(1, '\u6b63\u5e38'), (2, '\u5220\u9664'), (3, '\u8349\u7a3f')], default=1, verbose_name='\u72b6\u6001')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='\u5206\u7c7b')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u4f5c\u8005')),
            ],
            options={
                'verbose_name': '\u6587\u7ae0',
                'verbose_name_plural': '\u6587\u7ae0',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10, verbose_name='\u540d\u79f0')),
                ('status', models.PositiveIntegerField(choices=[(1, '\u6b63\u5e38'), (2, '\u5220\u9664')], default=1, verbose_name='\u72b6\u6001')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u4f5c\u8005')),
            ],
            options={
                'verbose_name': '\u6807\u7b7e',
                'verbose_name_plural': '\u6807\u7b7e',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='tag',
            field=models.ManyToManyField(to='blog.Tag', verbose_name='\u6807\u7b7e'),
        ),
    ]