from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserManager, User

def index(request):
    return render(request, "thegame/index.html")

def register(request):
    User.objects.register(request)
    return redirect('/')

def login(request):
    if User.objects.userLogin(request):
        return redirect('/home')
    else:
        return redirect('/')



def home(request):
    users = User.objects.all()
    context = {
    'users': users,
    }
    return render(request, "thegame/homepage.html", context)
