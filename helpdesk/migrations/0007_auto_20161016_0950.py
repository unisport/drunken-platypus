# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-16 09:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('helpdesk', '0006_issuehistory_issue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuehistory',
            name='issue',
        ),
        migrations.DeleteModel(
            name='IssueHistory',
        ),
    ]