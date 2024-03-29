# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-12 09:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20170312_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_post',
            field=models.BooleanField(default=False, verbose_name='是否发表'),
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='分类'),
        ),
    ]
