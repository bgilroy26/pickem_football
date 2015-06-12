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
    marquee = models.ImageField(blank=True, upload_to = 'game/static/league')
    slug = models.SlugField()

    def to_json(self):
        return {'name':self.name,'buy_in':self.buy_in, 'created_at':self.created_at, 'updated_at':self.updated_at, 'commissioner':self.commissioner, 'nfl_year':self.nfl_year,'slug':self.slug,'marquee':self.marquee}


class Team(models.Model):
    name = models.CharField(max_length=75,default=None,unique=True)
    mascot = models.ImageField(blank=True, upload_to = 'game/static/team')
    manager = models.ForeignKey(User)
    league = models.ForeignKey(League)
    wins = models.IntegerField()
    losses = models.IntegerField()
    slug = models.SlugField()
    champion = models.BooleanField(default=False)

    def get_record(self):
        return str(self.wins, '-', self.losses)

    def to_json(self):
        return {'name':self.name,'manager':self.manager,'mascot':self.mascot,'commissioner':self.commissioner,
        'slug':self.slug,'wins':self.wins,'losses':self.losses,'league':self.league,}


class TeamPick(models.Model):
    nfl_week = models.IntegerField()
    choice = models.CharField(max_length=70)
    correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    team = models.ForeignKey(Team)
