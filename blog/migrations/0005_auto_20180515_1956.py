# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-05-15 16:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20180515_1954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='status',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
