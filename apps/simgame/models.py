# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..login_and_register.models import User


# Create your models here.
class Game(models.Model):
    winner = models.ForeignKey(User, related_name = "wins", blank=True, null=True)   #This is the only place where 
    loser = models.ForeignKey(User, related_name = "losses", blank=True, null=True)  #Wins and losses need to be tracked. 
    points_win = models.IntegerField(default = 0)
    points_lose = models.IntegerField(default = 0)
    win_exp = models.IntegerField(default = 0)
    lose_exp = models.IntegerField(default = 0)
    win_tot_exp = models.IntegerField(default = 0)
    lose_tot_exp = models.IntegerField(default = 0)
    win_skill = models.IntegerField(default = 0)
    lose_skill = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)