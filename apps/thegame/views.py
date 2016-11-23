from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Usermanager, User

def index(request):
    return render(request, "thecave/index.html")

def register(request):
    if UserManager.isValid(request.POST, request):
        valid == True
        return redirect('/')
    else:
        return redirect('/')

def login(request):
    if UserManager.userLogin(request.POST, request):
        valid == True
        return redirect('/home')
    else:
        return redirect('/')



def home(request):
    users = User.objects.all()
    context = {
    'users': users,
    }
    return render(request, "thecave/homepage.html", context)
