# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-21 20:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_auto_20170320_2107'),
    ]

    operations = [
        migrations.CreateModel(
            name='Master',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='姓名')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='邮箱')),
                ('mobile', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话')),
                ('jobnum', models.CharField(blank=True, max_length=11, null=True, verbose_name='工号')),
                ('job', models.CharField(blank=True, max_length=100, null=True, verbose_name='业务')),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Category', verbose_name='分类'),
        ),
    ]
