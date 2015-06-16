from game.models import TeamPick

def get_weekly_record(week,team):
    wins = len(TeamPick.objects.filter(correct=True,nfl_week=week,team=team))
    losses = len(TeamPick.objects.filter(correct=False,nfl_week=week,team=team))
    team_weekly_record_dict = {'wins':wins, 'losses':losses}
    return team_weekly_record_dict
