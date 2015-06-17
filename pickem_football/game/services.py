from game.models import TeamPick,Team


def get_weekly_record(week,team):

    wins = len(TeamPick.objects.filter(correct=True,nfl_week=week,team=team))
    losses = len(TeamPick.objects.filter(correct=False,nfl_week=week,team=team))
    team_weekly_record_dict = {'wins':wins, 'losses':losses}

    return team_weekly_record_dict


def tally_weekly_results(week, team, winners_dict):

    team_picks_list = TeamPick.objects.filter(team=team,nfl_week=week)

    team = Team.objects.filter(name=team.name)[0]

    pick_list_dict = {'weekly_picks': [pick.choice for pick in team_picks_list]}

    winning_teams_list = winners_dict['winning_teams']

    print([x.choice for x in team_picks_list])

    for nfl_team_pick in team_picks_list:
        print(nfl_team_pick.choice)
        if TeamPick.objects.filter(team=team, nfl_week= week, choice = nfl_team_pick.choice, was_counted=False):
            if nfl_team_pick.choice in winning_teams_list:
                nfl_team_pick.correct = True
                team.wins += 1
            else:
                team.losses += 1

            team.save()
            nfl_team_pick.was_counted = True
            nfl_team_pick.save()
            team.save()

    return pick_list_dict
