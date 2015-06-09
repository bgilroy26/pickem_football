from django.db import models
from users.models import User
# Create your models here.

class League(models.Model):
    name = models.CharField(max_length=200,unique=True)
    buy_in = models.DecimalField(max_digits = 20, decimal_places = 8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    commissioner = models.ForeignKey(User)
    slug = models.SlugField()

class Membership(models.Model):
    member = models.ForeignKey(User)
    league = models.ForeignKey(League)
    team_name = models.CharField(max_length=75,default=None)
    team_pic = models.ImageField(default=None)

class WeeklyPicks(models.Model):
    membership = models.ForeignKey(Membership)
    wins = models.IntegerField(Default=0)
    losses = models.IntegerField(Default=0)

class Game(models.Model):
    hometeam = models.CharField(max_length=70)
    awayteam = models.CharField(max_length=70)
    correct = models.BooleanField(Default=False)
    homescore = models.IntegerField()
    awayscore = models.IntegerField()
    week = models.ForeignKey(WeeklyPicks)
