# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-01-20 18:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0039_log_scrennid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log',
            old_name='ScrennId',
            new_name='ScreenId',
        ),
    ]