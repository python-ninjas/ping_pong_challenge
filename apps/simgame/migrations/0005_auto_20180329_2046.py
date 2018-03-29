# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-03-29 20:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('simgame', '0004_auto_20180329_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='loser',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='losses', to='login_and_register.User'),
        ),
        migrations.AlterField(
            model_name='game',
            name='winner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wins', to='login_and_register.User'),
        ),
    ]