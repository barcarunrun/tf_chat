# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-01-16 00:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0021_auto_20190116_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qa',
            name='is_public',
            field=models.CharField(choices=[('1', '公開'), ('0', 'テスト')], default='0', max_length=10),
        ),
    ]
