from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class League(models.Model):
    name = models.CharField(max_length=200,unique=True)
    buy_in = models.DecimalField(max_digits = 20, decimal_places = 8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    commissioner = models.ForeignKey(User)
    nfl_year = models.IntegerField()
    slug = models.SlugField()

class Team(models.Model):
    name = models.CharField(max_length=75,default=None)
    pic = models.ImageField(default=None)
    manager = models.ForeignKey(User)
    league = models.ForeignKey(League)

class TeamPick(models.Model):
    nfl_week = models.IntegerField()
    choice = models.CharField(max_length=70)
    correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    team = models.ForeignKey(Team)
