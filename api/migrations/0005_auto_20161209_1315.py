# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-09 13:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20161209_1105'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='joined_users',
            new_name='users',
        ),
    ]
