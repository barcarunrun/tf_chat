# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-20 18:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0038_auto_20190116_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='ScrennId',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]