# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-25 13:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0013_auto_20161024_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(choices=[(b'OPEN', b'Open'), (b'CLOSED', b'Closed'), (b'ONHOLD', b'On Hold')], default=b'OPEN', max_length=100),
        ),
    ]
