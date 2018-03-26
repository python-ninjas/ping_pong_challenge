# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_and_register.models import User


# Create your models here.
class Games(models.Model):
    winner = models.ForeignKey(User, related_name = "wins")
    loser = models.ForeignKey(User, related_name = "losses")
    points_win = models.IntegerField()
    points_lose = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)