from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserManager, User, MarkovChain

def index(request):
    if 'user_id' not in request.session:
        request.session['user_id'] = 0
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

    try:
        User.objects.get(id = request.session['user_id'])
    except:
        return redirect('/')

    text = MarkovChain()
    text.add_file('apps/thegame/text.txt')
    content = text.generate_text()
    context = {
    'users': users,
    'contents': content
    }
    return render(request, "thegame/homepage.html", context)

def logout(request):
    request.session.delete()
    return redirect('/')
