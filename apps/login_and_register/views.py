from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from ..simgame.models import Game
from models import *
import pygal
from pygal.style import Style
custom_style = Style(
    title_font_size=30,
    legend_font_size=30,
    label_font_size=25,
    )

# Create your views here.
def index(request):
    if 'id' not in request.session or request.session['id'] == 0 :
        request.session['id'] = 0
        return render(request,'login_and_register/index.html')
    elif request.session['id'] > 0:
        return redirect('/home')
    

def login(request):
    if request.method != 'POST':
        return redirect('./')

    errors = []

    username = request.POST['username']
    # pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())

    if len(User.objects.filter(username=username)) > 0:
        if bcrypt.checkpw(request.POST['password'].encode(), User.objects.filter(username=username).first().pw_hash.encode()):
            print "Password MATCHES"
            user = User.objects.filter(username=username).first()
            request.session["id"] = user.id
            messages.success(request, 'Successfully logged in!')
            return redirect('./success')
        else:
            print "Password is incorrect!"
            messages.error(request, 'Password is incorrect.')
    else:
        print "User does not exist!"
        messages.error(request, 'User does not exist.')    
    return redirect('./')

def logout(request):
    request.session.clear()
    return redirect('./')

def success(request):
    no_messages = True
    messages = get_messages(request)
    for message in messages:
        no_messages = False
        break
    if 'id' not in request.session or no_messages:
        return redirect('./')
    context = {
        'user': User.objects.filter(id = request.session['id']).first()
    }
    return render(request,'login_and_register/success.html',context)

def register(request):
    if request.method != 'POST':
        return redirect('./')
    response = User.objects.validateRegistration(request.POST)
    if response['status']:
        messages.success(request,'Registration Successful!')
        request.session.clear()
        request.session["id"] = response['user_id']
        return redirect('./success')
    if 'errors' in response:
        for error in response['errors']:
            messages.error(request,error)
        for key in response['feedback']:
            request.session[key] = response['feedback'][key]
        return redirect('./')

def home(request):
    if 'id' not in request.session:
        return redirect('./')
    try:
        user = User.objects.filter(id = request.session['id']).first()
        context = {
            'user': user,
            'wins': user.wins.count(),
            'losses': user.losses.count(),
            'opponents': User.objects.exclude(id=request.session['id']).order_by("-skill")
        }
    except Exception as e:
        return redirect('./')
    return render(request,'login_and_register/home.html',context)
# routes for user charts below:
def userskillchart(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        allusers = User.objects.all()
        totalusers = User.objects.all().count()
        topuser = User.objects.order_by('skill').reverse()[:1]
        attrsum = 0
        userchart = pygal.Bar(legend_box_size=25, style=custom_style)
        for user in allusers:
            attrsum += user.skill
        userchart.title =  "Skill Levels"
        userchart.add('You', user.skill)
        userchart.add("Average Player", attrsum/totalusers)
        userchart.add("Top Player", topuser[0].skill)
        userchart.render_to_file('apps/login_and_register/static/login_and_register/img/userchart.svg')
    return redirect("/home")

def userexpchart(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        allusers = User.objects.all()
        totalusers = User.objects.all().count()
        topuser = User.objects.order_by('experience').reverse()[:1]
        attrsum = 0
        userchart = pygal.Bar(legend_box_size=25, style=custom_style)
        for user in allusers:
            attrsum += user.experience
        userchart.title =  "Experience"
        userchart.add('You', user.experience)
        userchart.add("Average Player", attrsum/totalusers)
        userchart.add("Top Player", topuser[0].experience)
        userchart.render_to_file('apps/login_and_register/static/login_and_register/img/userchart.svg')
    return redirect("/home")

def userpointschart(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        allusers = User.objects.all()
        totalusers = User.objects.all().count()
        topuser = User.objects.order_by('totalscore').reverse()[:1]
        attrsum = 0
        userchart = pygal.Bar(legend_box_size=25, style=custom_style)
        for user in allusers:
            attrsum += user.totalscore
        userchart.title =  "Total Points Scored"
        userchart.add('You', user.totalscore)
        userchart.add("Average Player", attrsum/totalusers)
        userchart.add("Top Player", topuser[0].totalscore)  
        userchart.render_to_file('apps/login_and_register/static/login_and_register/img/userchart.svg')
    return redirect("/home")
def userwinratiochart(request):
    if request.method == 'POST':
        usergamewins = Game.objects.filter(winner=request.session["id"]).count()
        usergamewins = usergamewins*1.00
        usergamelosses = Game.objects.filter(loser=request.session["id"]).count()
        usergamelosses = usergamelosses*1.00
        allusers = User.objects.all()
        print allusers
        totalusers = User.objects.all().exclude(totalscore=0).count()
        topuser = Game.objects.order_by('wins').reverse()[:1]
        attrsum = 0.00
        userchart = pygal.Bar(legend_box_size=25, style=custom_style)
        topuser = 0.00
        for user in allusers:
            userwins = Game.objects.filter(winner= user).count()
            userwins = userwins*1.00
            userlosses = Game.objects.filter(loser= user).count()
            userlosses = userlosses*1.00
            if userlosses == 0 and userwins == 0:
                continue
            attrsum += userwins/userlosses
            if userwins/userlosses > topuser:
                topuser = userwins/userlosses
        print attrsum
        userchart.title =  "Win/Loss Ratios"
        if usergamewins == 0 and usergamelosses == 0:
            userchart.add('You', 0)
        else:
            userchart.add('You', usergamewins/usergamelosses)
        userchart.add("Average", attrsum/totalusers)
        userchart.add("Top Player", topuser)    
        userchart.render_to_file('apps/login_and_register/static/login_and_register/img/userchart.svg')
    return redirect("/home")
##### Below is for all other opponents chart
def alloppskillchart(request):
    if request.method == 'POST':
        opponents = User.objects.exclude(id=request.session['id']).order_by("-skill")
        alloppchart = pygal.Bar(legend_box_size=25, style=custom_style)
        alloppchart.title = "Skill Levels"
        for user in opponents:
            print user
            alloppchart.add(user.first_name+user.last_name, user.skill)
        alloppchart.render_to_file('apps/login_and_register/static/login_and_register/img/alloppchart.svg')
    return redirect("/home")

def alloppexpchart(request):
    if request.method == 'POST':
        opponents = User.objects.exclude(id=request.session['id']).order_by("-skill")
        alloppchart = pygal.Bar(legend_box_size=25, style=custom_style)
        alloppchart.title = "Experience"
        for user in opponents:
            alloppchart.add(user.first_name+user.last_name, user.experience)
        alloppchart.render_to_file('apps/login_and_register/static/login_and_register/img/alloppchart.svg')
    return redirect("/home")

def allopp_pointschart(request):
    if request.method == 'POST':
        opponents = User.objects.exclude(id=request.session['id']).order_by("-skill")
        alloppchart = pygal.Bar(legend_box_size=25, style=custom_style)
        alloppchart.title = "Total Points"
        for user in opponents:
            alloppchart.add(user.first_name+user.last_name, user.totalscore)
        alloppchart.render_to_file('apps/login_and_register/static/login_and_register/img/alloppchart.svg')
    return redirect("/home")