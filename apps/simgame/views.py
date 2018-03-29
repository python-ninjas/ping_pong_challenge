from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core import serializers
from ..login_and_register.models import User
from models import *
import random

def index(request):
    if 'id' not in request.session or request.session['id'] == 0 :
        return redirect('/')
    user = User.objects.filter(id = request.session['id']).first()
    upperbound = user.skill * 4
    lowerbound = user.skill / 4
    context = {
        'user': user,
        'opponents': User.objects.exclude(id=request.session['id'], skill__gt = upperbound, skill__lt = lowerbound).order_by("-skill")
    }
    return render(request,'simgame/index.html',context)

# STATS

def stats(request):
    if 'id' not in request.session or request.session['id'] == 0 :
        return redirect('/')
    user = User.objects.filter(id = request.session['id']).first()
    context = {
        'user': user,
        'opponents': User.objects.exclude(id=request.session['id']).order_by("-skill")
    }   
    return render(request,'simgame/stats.html',context)

def load_stats(request):
    games = Game.objects.all()
    return render(request,'simgame/results_table.html',{"games": games})

def find_stats(request): 
    user_id = request.session['id']
    opponent_id = request.POST['opponent']
    wins = Game.objects.filter(winner__id=user_id).filter(loser__id=opponent_id).order_by("-created_at")
    losses = Game.objects.filter(loser__id=user_id).filter(winner__id=opponent_id).order_by("-created_at")
    games = wins | losses        
    if request.POST['search_by'] == 'Games You Won':
        games = wins
    if request.POST['search_by'] == 'Games You Lost':
        games = losses
    return render(request,'simgame/results_table.html',{'games': games})

# GAMEPLAY

def play(request):
    request.session['opp_id'] = request.POST['opp_id']
    request.session['max_points'] = int(request.POST['max_points'])
    print request.session['max_points']
    p1points = 0
    p2points = 0 #Player making the challenge is always player 1. 
    x = User.objects.get(id=int(request.session['id']))
    p1skill = float(x.skill)
    if request.POST['opp_id'] == "dummy":
        p2skill = p1skill
    else: 
        y = User.objects.get(id=int(request.session['opp_id']))
        p2skill = float(y.skill)
    while abs(p1points - p2points) < 2 or (p1points < request.session['max_points'] and p2points < request.session['max_points']):
        chance = p1skill/(p1skill + p2skill)
        rand_num = random.random()
        if rand_num < chance: 
            p1points += 1
        else: 
            p2points += 1
    
    x.totalscore += p1points
    x.experience += p1points
    if request.POST['opp_id'] != "dummy":
        y.totalscore += p2points
        y.experience += p2points
    if p1points > p2points:
        if(request.POST['opp_id'] != "dummy"):
            win_exp = 10*y.skill
            lose_exp = 2*x.skill
            x.experience += win_exp
            y.experience += lose_exp
            Game.objects.create(winner=x, loser=y,points_win=p1points,points_lose=p2points,win_exp = win_exp, lose_exp = lose_exp)
        else:
            win_exp = 5 * x.skill
            lose_exp = 1 * x.skill
            x.experience += win_exp
            Game.objects.create(winner=x,points_win=p1points,points_lose=p2points,win_exp = win_exp, lose_exp = lose_exp)
        messages.success(request,'You win! Congratulations!')
    else: 
        if(request.POST['opp_id'] != "dummy"):
            lose_exp = 2*y.skill
            win_exp = 10*x.skill
            x.experience += lose_exp
            y.experience += win_exp
            Game.objects.create(winner=y, loser=x,points_win=p2points,points_lose=p1points,win_exp = win_exp, lose_exp = lose_exp)
        else:
            lose_exp = x.skill
            win_exp = 5*x.skill
            x.experience+=lose_exp
            Game.objects.create(loser=x,points_win=p2points,points_lose=p1points,win_exp = win_exp, lose_exp = lose_exp)
        messages.success(request,'You lose! Better luck next time!')
    while x.experience >= x.skill * 50 + 1:
        x.experience -= x.skill * 50 + 1     #Level up! Accounts for gaining multiple levels in a single game, too. 
        x.skill += 1
        x.save()
    if(request.POST['opp_id'] != "dummy"):
        while y.experience >= y.skill * 50 + 1:
            y.experience -= y.skill * 50 + 1    
            y.skill += 1
            y.save()
    if p1points > p2points:
        messages.success(request,'Score: {} to {}'.format(p1points,p2points))
    else:
        messages.error(request,'Score: {} to {}'.format(p1points,p2points))
    return redirect('/game/result')

def result(request):
    context = {
        'user': User.objects.filter(id = request.session['id']).first(),
        'opponent': User.objects.filter(id = request.session['opp_id']).first()
    }
    return render(request, 'simgame/result.html',context)