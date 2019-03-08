# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-03-05 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20190216_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='last_score',
            field=models.FloatField(default=0, verbose_name='最新分数'),
        ),
        migrations.AlterField(
            model_name='team',
            name='max_score',
            field=models.FloatField(default=0, verbose_name='最高分'),
        ),
    ]