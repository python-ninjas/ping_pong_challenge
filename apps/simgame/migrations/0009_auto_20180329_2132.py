# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-29 21:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simgame', '0008_auto_20180329_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='lose_exp',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='game',
            name='lose_skill',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='game',
            name='lose_tot_exp',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='game',
            name='points_lose',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='game',
            name='points_win',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='game',
            name='win_exp',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='game',
            name='win_skill',
            field=models.IntegerField(default=None),
        ),
        migrations.AlterField(
            model_name='game',
            name='win_tot_exp',
            field=models.IntegerField(default=None),
        ),
    ]
