# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-28 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simgame', '0002_auto_20180327_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='lose_exp',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='game',
            name='win_exp',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='points_lose',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='game',
            name='points_win',
            field=models.IntegerField(default=0),
        ),
    ]