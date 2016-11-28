from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserManager, User, MarkovChain
import random

text = MarkovChain()
text.add_file('apps/thegame/texts/text1.txt')
text.add_file('apps/thegame/texts/text2.txt')
text.add_file('apps/thegame/texts/text3.txt')
text.add_file('apps/thegame/texts/text4.txt')
text.add_file('apps/thegame/texts/text5.txt')
text.add_file('apps/thegame/texts/text6.txt')

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
    users = User.objects.all().order_by('-highscore')

    request.session['health'] = 100
    request.session['gold'] = 0
    request.session['cave'] = 1
    #highscores = User.objects.all().orderby(highscore)

    try:
        User.objects.get(id = request.session['user_id'])
    except:
        return redirect('/')

    return render(request, "thegame/homepage.html", {'users': users})

def action(request):
    direction = request.POST['direction']
    gold = 0
    health = 0

    if direction == 'left':
        gold = random.randrange(10,51)
        health = random.randrange(-5,1)
    else:
        gold = random.randrange(25,51)
        health = random.randrange(-10,1)

    request.session['gold'] += gold
    request.session['health'] += health
    request.session['cave'] += 1
    content = text.generate_text()

    context = {
    'gold': request.session['gold'],
    'health': request.session['health'],
    'cave': request.session['cave'],
    'contents': content
    }

    if request.session['health'] < 0:
        return redirect('/lost')
    else:
        return render(request, "thegame/cave.html", context)

def lost(request):
    score = int(request.session['gold']) + 5*int((request.session['cave']))
    currentuser = User.objects.get(id = request.session['user_id'])
    if currentuser.highscore < score:
        User.objects.filter(id = request.session['user_id']).update(highscore= score)
    else:
        pass

    context = {
    'gold': request.session['gold'],
    'cave': request.session['cave'],
    'highscore': score,
    }
    return render(request, "thegame/lost.html", context)


def enter(request):
    return redirect('/cave')

def cave(request):
    content = text.generate_text()
    return render(request, "thegame/cave.html", {'contents': content})

def logout(request):
    request.session.delete()
    return redirect('/')
