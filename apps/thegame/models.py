from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt
import re

#login alias = alias
#login password name = password
#register name = reg_name
#register alias = reg_alias
#register password name = reg_password
#register confirm password name = reg_password2

class UserManager(models.Manager):
    def isValid(self, request):
        name = request.POST['reg_name']
        alias = request.POST['reg_alias']
        email = request.POST['email']
        birthdate = request.POST['birthdate']
        today = date.today()
        reg_password = request.POST['reg_password']
        reg_password2 = request.POST['reg_password2']
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        valid = False

        if len(name) < 1:
            messages.warning(request, "Name cannot be blank.")
            valid = False
        elif len(alias) < 1:
            messages.warning(request, "Alias cannot be blank.")
            valid = False
        elif not re.match(regex, email):
            messages.warning(request, "Invalid Email.")
            valid = False
        elif len(reg_password) < 8:
            messages.warning(request, "Password must be longer than 8 characters.")
            valid = False
        elif reg_password != reg_password2:
            messages.warning(request, "Passwords do not match")
            valid = False
        elif (birthdate.year + 13, birthdate.month, birthdate.day) > (today.year, today.month, today.day):
            messages.warning(request, "You must be at least 13 to play this game!")
            valid = False
        elif Users.objects.filter(alias = alias):
            messages.warning(request, "Alias is already taken.")
            valid = False
        elif Users.objects.filter(email = email):
            messages.warning(request, "You have registered with this email before, Please login.")
            valid = False
        else:
            valid = True

        if valid == True:
        hashedpw = bcrypt.hashpw(reg_password.encode('UTF-8'), bcrypt.gensalt())
        makeuser = Users.objects.create(name = name, alias = alias, email = email, birthdate= birthdate, password = hashedpw)
        messages.success(request, "You have successfully registered, please Login.")
        return valid


    def userLogin(self, request):
        alias = request.POST['alias']
        loginpassword = request.POST['password']
        valid = False

        if len(alias) < 1:
            messages.warning(request, "Alias cannot be blank!")
            valid = False
        if len(loginpassword) < 1:
            messages.warning(request, "Password cannot be blank!")
            valid = False
        try:
            user = Users.objects.get(alias = alias)
        #doesn't break if it fails
        except:
            messages.warning(request, "Users does not exist!")
            valid = False
        #if user exists log them in by checking hashed password
        if bcrypt.hashpw(loginpassword.encode(), user.password.encode()) == user.password.encode():
            #lets keep that user information for later
            request.session['user_id'] = user.id
            request.session['alias'] = user.alias
            valid = True
        else:
            messages.warning(request, "Password is incorrect!")
            valid = False
        return valid


class Users(models.Model):
      name = models.CharField(max_length=45, default='')
      alias = models.CharField(max_length=45, default='')
      email = models.CharField(max_length=45, default='')
      password = models.CharField(max_length=200, default='')
      birthdate = models.CharField(max_length=45, default='')
