from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.messages import get_messages
from models import *
from ..login_and_register.models import User

# Create your views here.
def index(request):
    if 'id' not in request.session:
        request.session['id'] = 0
    context = {
        'user': User.objects.filter(id = request.session['id']).first()
    }
    return render(request,'login_and_register/index.html',context)

def play(request):
    return redirect('/')

def result(request):
    return redirect('/')