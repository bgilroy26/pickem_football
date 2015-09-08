from django.db import models
from django.contrib.auth.models import User


class League(models.Model):
    name = models.CharField(max_length=200,unique=True)
    buy_in = models.DecimalField(max_digits = 20, decimal_places = 2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    commissioner = models.ForeignKey(User)
    nfl_year = models.IntegerField(default=2015)
    marquee = models.ImageField(blank=True, default='rose-bowl.jpg', upload_to = 'static/league')
    slug = models.SlugField()

    def to_json(self):
        return {'name':self.name,'buy_in':self.buy_in, 'created_at':self.created_at, 'updated_at':self.updated_at, 'commissioner':self.commissioner.username, 'nfl_year':self.nfl_year,'slug':self.slug,'marquee':self.marquee.name}


class Team(models.Model):
    name = models.CharField(max_length=100,default=None)
    mascot = models.ImageField(default='download.jpg', upload_to = 'static/team')
    manager = models.ForeignKey(User)
    league = models.ForeignKey(League)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    champion = models.BooleanField(default=False)
    slug = models.SlugField()

    def get_season_record(self):
        return str(self.wins, '-', self.losses)


    def to_json(self):
        return {'name':self.name,'manager':self.manager.username,'mascot':self.mascot.name,
        'slug':self.slug,'wins':self.wins,'losses':self.losses,'league':self.league.name}


class TeamPick(models.Model):
    nfl_week = models.IntegerField()
    game_id = models.IntegerField()
    choice = models.CharField(max_length=70,blank=True)
    correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    was_counted = models.BooleanField(default=False)
    team = models.ForeignKey(Team)

    def to_json(self):
        import json
        return json.dumps({"nfl_week":self.nfl_week,"choice":self.choice,"correct":self.correct,"team":self.team.name,
        "created_at":self.created_at.isoformat(),"updated_at":self.updated_at.isoformat()})
