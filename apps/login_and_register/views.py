from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from models import *

# Create your views here.
def index(request):
    if 'id' not in request.session or request.session['id'] == 0 :
        request.session['id'] = 0
        return render(request,'login_and_register/index.html')
    elif request.session['id'] > 0:
        context = {
            'user': User.objects.filter(id = request.session['id']).first()
        }
        return render(request,'login_and_register/home.html',context)
    

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
    context = {
        'user': User.objects.filter(id = request.session['id']).first()
    }
    return render(request,'login_and_register/home.html',context)