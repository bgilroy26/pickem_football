from game.models import Team, League
from users.models import User
from django.forms import ModelForm

class LeagueForm(ModelForm):
    class Meta:
        model = League
        fields = ['name','buy_in', 'marquee']


class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'mascot']
