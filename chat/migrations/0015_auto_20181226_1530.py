# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2018-12-26 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0014_qa_is_public'),
    ]

    operations = [
        migrations.AlterField(
            model_name='qa',
            name='is_public',
            field=models.CharField(choices=[('0', 'テスト'), ('1', '公開')], max_length=1),
        ),
    ]
