from __future__ import unicode_literals
from collections import defaultdict, deque
from django.db import models
from django.contrib import messages
from datetime import datetime
import codecs
import random
import bcrypt
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')
SENTENCE_SEPARATOR = '.'
WORD_SEPARATOR = ' '

#login alias = alias
#login password name = password
#register name = reg_name
#register alias = reg_alias
#register password name = reg_password
#register confirm password name = reg_password2

class UserManager(models.Manager):
    def register(self, request):
        name = request.POST['reg_name']
        alias = request.POST['reg_alias']
        email = request.POST['email']
        today = datetime.today()
        reg_password = request.POST['reg_password']
        reg_password2 = request.POST['reg_password2']
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        valid = True

        if not name:
            messages.warning(request, "Name cannot be blank.")
            valid = False
        if not alias:
            messages.warning(request, "Alias cannot be blank.")
            valid = False
        if not re.match(regex, email):
            messages.warning(request, "Invalid Email.")
            valid = False
        if len(reg_password) < 8:
            messages.warning(request, "Password must be longer than 8 characters.")
            valid = False
        if reg_password != reg_password2:
            messages.warning(request, "Passwords do not match")
            valid = False
        if not request.POST['birthdate']:
            messages.warning(request, "The Birthdate cannot be blank")
        else:
            birthdate = datetime.strptime(request.POST['birthdate'], '%Y-%m-%d')
            if (birthdate.year + 13, birthdate.month, birthdate.day) > (today.year, today.month, today.day):
                messages.warning(request, "You must be at least 13 to play this game!")
                valid = False
        if User.objects.filter(alias = alias):
            messages.warning(request, "Alias is already taken.")
            valid = False
        if User.objects.filter(email = email):
            messages.warning(request, "You have registered with this email before, Please login.")
            valid = False

        if valid == True:
            hashedpw = bcrypt.hashpw(reg_password.encode('UTF-8'), bcrypt.gensalt())
            makeuser = User.objects.create(name = name, alias = alias, email = email, birthdate= birthdate, password = hashedpw)
            messages.success(request, "You have successfully registered, please Login.")


    def userLogin(self, request):
        alias = request.POST['alias']
        loginpassword = request.POST['password']
        valid = False

        if len(alias) < 1:
            messages.warning(request, "Alias cannot be blank!")
            return False
        if len(loginpassword) < 1:
            messages.warning(request, "Password cannot be blank!")
            return False
        try:
            user = User.objects.get(alias = alias)
        #doesn't break if it fails
        except:
            messages.warning(request, "User does not exist!")
            return False
        #if user exists log them in by checking hashed password
        if bcrypt.hashpw(loginpassword.encode(), user.password.encode()) == user.password.encode():
            #lets keep that user information for later
            request.session['user_id'] = user.id
            request.session['alias'] = user.alias
            return True
        else:
            messages.warning(request, "Password is incorrect!")
            return False

class User(models.Model):
      name = models.CharField(max_length=45, default='')
      alias = models.CharField(max_length=45, default='')
      email = models.CharField(max_length=45, default='')
      password = models.CharField(max_length=200, default='')
      birthdate = models.DateField()
      objects = UserManager()

class MarkovChain:

  def __init__(self, num_key_words=3):
    self.num_key_words = num_key_words
    self.lookup_dict = defaultdict(list)
    self._punctuation_regex = re.compile('[,.!;\?\:\-\[\]\n]+')
    self._seeded = False
    self.__seed_me()

  def __seed_me(self, rand_seed=None):
    if self._seeded is not True:
      try:
        if rand_seed is not None:
          random.seed(rand_seed)
        else:
          random.seed()
        self._seeded = True
      except NotImplementedError:
        self._seeded = False

  def add_file(self, file_path):
    content = ''
    with open(file_path, 'r') as fh:
      self.__add_source_data(fh.read())

  def add_string(self, str):
    self.__add_source_data(str)

  def __add_source_data(self, str):
    clean_str = self._punctuation_regex.sub(' ', str).lower()
    tuples = self.__generate_tuple_keys(clean_str.split())
    for t in tuples:
      self.lookup_dict[t[0]].append(t[1])

  def __generate_tuple_keys(self, data):
    if len(data) < self.num_key_words:
      return

    for i in xrange(len(data) - self.num_key_words):
      yield [ tuple(data[i:i+self.num_key_words]), data[i+self.num_key_words] ]

  def generate_text(self, max_length=8):
    context = deque()
    output = []
    if len(self.lookup_dict) > 0:
      self.__seed_me(rand_seed=len(self.lookup_dict))

      idx = random.randint(0, len(self.lookup_dict)-1)
      chain_head = list(self.lookup_dict.keys()[idx])
      context.extend(chain_head)

      while len(output) < (max_length - self.num_key_words):
        next_choices = self.lookup_dict[tuple(context)]
        if len(next_choices) > 0:
          next_word = random.choice(next_choices)
          context.append(next_word)
          output.append(context.popleft())
        else:
          break
      output.extend(list(context))
    return output
