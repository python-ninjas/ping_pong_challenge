from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from models import *
from ..login_and_register.models import User
from random import *

# Create your views here.
def index(request):
    context = {
        'opponents' : User.objects.exclude(id=request.session['id'])
    }
   
    return render(request,'simgame/index.html',context)

def play(request):
    p1points = 0
    p2points = 0 #Player making the challenge is always player 1. 
    p1skill = User.objects.get(id=request.session['id']).skill
    p2skill = User.objects.get(id=request.POST['opp_id']).skill
    while abs(p1points - p2points) < 2 or (p1points < request.POST['maxpoints'] and p2points < request.POST['maxpoints']):
        chance = p1skill/(p1skill + p2skill)
        if random.random() < chance: 
            p1points += 1
        else: 
            p2points += 1
    x = User.objects.get(id=request.session['id'])
    y = User.objects.get(id=request.POST['opp_id'])
    x.totalpoints += p1points
    x.experience += p1points
    y.totalpoints += p2points
    y.experience += p2points
    if p1points > p2points:
        Game.objects.create(winner=x, loser=y,points_win=p1points,points_lose=p2points)
        x.experience += 10 * y.skill
        y.experience += 2 * x.skill
        messages.success(request,'You win! Congratulations!')
    else: 
        Game.objects.create(winner=y, loser=x,points_win=p2points,points_lose=p1points)
        x.experience += 2 * y.skill
        y.experience += 10 * x.skill
        messages.success(request,'You lose! Better luck next time!')
    while x.experience >= x.skill * 30:
        x.experience -= x.skill * 30     #Level up! Accounts for gaining multiple levels in a single game, too. 
        x.skill += 1
    while y.experience >= y.skill * 50:
        y.experience -= y.skill * 50     
        y.skill += 1
    x.save()
    y.save()
    messages.success(request,'Score: {} to {}'.format(p1points,p2points))
    return redirect('/play/result')

def result(request):
    return render(request, '/simgame/result.html')