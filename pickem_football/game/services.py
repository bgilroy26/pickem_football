from game.models import TeamPick,Team


def get_weekly_record(week,team):

    wins = len(TeamPick.objects.filter(correct=True,nfl_week=week,team=team))
    losses = len(TeamPick.objects.filter(correct=False,nfl_week=week,team=team))
    team_weekly_record_dict = {'wins':wins, 'losses':losses}

    return team_weekly_record_dict


def tally_weekly_results(week, team, winners_list):

    team_picks_list = TeamPick.objects.filter(team=team,nfl_week=week)

    pick_list_dict = {'weekly_picks': [pick.choice for pick in team_picks_list]}

    if team_picks_list:
        for nfl_team_pick in team_picks_list:
            if nfl_team_pick.was_counted == False:
                if nfl_team_pick.choice in winners_list:
                    nfl_team_pick.correct = True
                    team.wins += 1
                else:
                    team.losses += 1
                nfl_team_pick.was_counted = True
                nfl_team_pick.save()
                team.save()
    else:
        for game in range(len(winners_list)):
            TeamPick.objects.create(team=team, nfl_week=week, choice='', was_counted=True,game_id=game)
            for nfl_team_pick in TeamPick.objects.filter(team=team, nfl_week=week, choice='', was_counted=True,game_id=game):
                team.losses += 1
                nfl_team_pick.save()
                team.save()

    return pick_list_dict
