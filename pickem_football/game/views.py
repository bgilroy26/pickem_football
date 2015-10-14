from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import HttpResponse, JsonResponse,Http404
from game.models import League, Team, TeamPick
from users.models import User
from game.services import get_weekly_record,tally_weekly_results
from django.utils.text import slugify
import django.forms
import requests
import json
import os

class Selection():

    def __init__(self, id_num, team):
        self.num = id_num
        self.team = team

class ActiveTeamsView(View):

    def get(self,request,username):
        player_teams = Team.objects.filter(user__username=username,league__nfl_year=2015)
        return JsonResponse({'active_player_teams':player_teams})

class PastTeamsView(View):

    def get(self,request,username):
        player_teams = Team.objects.filter(user__username=username,league__nfl_year=year).exclude(league__nfl_year=2015)
        return JsonResponse({'past_player_teams':player_teams})

class InvitesView(View):

    def get(self,request,username):
        pending_leagues = Team.objects.filter(user__username=username,name=None)
        return JsonResponse({'pending_leagues':pending_leagues})

class WeeklyMatchupsView(View):

    def get(self,request,year,week):
        r = requests.get(os.environ.get('fballAPI') + year + '/' + week + '/matchups/')
        string_dict = r.content.decode("utf-8")
        matchup_dict = json.loads(string_dict)
        return JsonResponse({'matchup_dict':matchup_dict})

class WeeklyScoresView(View):

    def get(self, request, year, week):
        r = requests.get(os.environ.get('fballAPI') + year + '/' + week + '/scores/')
        string_dict = r.content.decode("utf-8")
        scores_dict = json.loads(string_dict)
        return JsonResponse({'scores_dict':scores_dict})

class TeamPickView(View):

    def get(self, request, year, week, team_slug):
        week_int = int(week.strip('week-'))
        r = requests.get(os.environ.get('fballAPI') + week + '/matchups/')

        string_dict = r.content.decode("utf-8")
        matchups_dict = json.loads(string_dict)
        current_team = Team.objects.filter(slug=team_slug)[0]
        team_dict = current_team.to_json()
        team_picks = TeamPick.objects.filter(team = current_team, nfl_week = week_int)

        pick_dict = {'{}_{}_picks'.format(current_team.slug, week):[pick.to_json() for pick in team_picks]}

        return JsonResponse({'team_dict':team_dict, 'matchups_dict':matchups_dict, 'weekly_picks':pick_dict})

    def post(self, request, year, week, team_slug):
        week_int = int(week.strip('week-'))
        current_team = Team.objects.filter(slug=team_slug)[0]

        choice_dict = request.POST.dict()
        choice_length = len(choice_dict.keys())
        picks_count = choice_length // 2
        keys_to_pull_by = sorted(choice_dict.keys())
        choice_list = [Selection(choice_dict['choices[' + str(i) + '][num]'], choice_dict['choices[' + str(i) + '][team]']) for i in range(picks_count)]

        for selected in choice_list:
            new_pick, created = TeamPick.objects.get_or_create(game_id=selected.num, team=current_team, nfl_week=week_int)
            if not created and new_pick.choice == selected.team:
                return JsonResponse({})
            new_pick.choice = selected.team
            new_pick.save()

        return JsonResponse({})

class WeeklyTeamResultsView(View):

    def get(self, request, year, week, team_slug):

        if request.session.get('_auth_user_id'):


            active_user_id = int(request.session.get('_auth_user_id'))
            active_user = User.objects.filter(id=active_user_id)[0]
            week_int = int(week.strip('week-'))

            r = requests.get(os.environ.get('fballAPI') + year + '/' + week + '/winners/')
            string_dict = r.content.decode("utf-8")
            winners_dict = json.loads(string_dict)

            current_team = Team.objects.filter(slug=team_slug)[0]
            team_dict = current_team.to_json()

            current_team_weekly_record_dict = get_weekly_record(week_int,current_team)

            pick_list_dict = tally_weekly_results(week_int, current_team, winners_dict)

            return JsonResponse({'current_team_weekly_record_dict':current_team_weekly_record_dict, 'team_dict':team_dict, 'winners_dict': winners_dict,'pick_list_dict':pick_list_dict})

class CreateLeagueView(View):

    def post(self, request, year):
        if request.session.get('_auth_user_id'):

            active_user_id = int(request.session.get('_auth_user_id'))
            active_user = User.objects.filter(id=active_user_id)[0]

            buy_in = request.POST['buy_in']
            name = request.POST['name']

            new_league = League(name=name, buy_in = buy_in, commissioner = active_user, nfl_year=year)

            new_league.slug = slugify(new_league.name)
            new_league.save()
            new_league_dict = new_league.to_json()

            if new_league:
                return JsonResponse({'Success':True, 'new_league_dict':new_league_dict})

            return JsonResponse({'Success':False})

class UpdateLeagueView(View):

    def post(self, request, league_slug):
        if request.session.get('_auth_user_id'):

            active_user_id = int(request.session.get('_auth_user_id'))
            active_user = User.objects.filter(id=active_user_id)[0]

            current_league = League.objects.filter(slug=league_slug)[0]

            if active_user == current_league.commissioner:

                name = request.POST['name']
                marquee = request.POST['marquee']

                current_league.name = name
                current_league.marquee = marquee
                current_league.slug = slugify(current_league.name)
                current_league.save()
                updated_league_dict = current_league.to_json()

                return JsonResponse({'Success':True, 'updated_league_dict':updated_league_dict})
            return JsonResponse({'Success':False})

class CreateTeamView(View):

    def post(self, request, league_slug):
        if request.session.get('_auth_user_id'):

            active_user_id = int(request.session.get('_auth_user_id'))
            active_user = User.objects.filter(id=active_user_id)[0]

            current_league = League.objects.filter(slug=league_slug)[0]

            name = request.POST['name']

            if not Team.objects.filter(manager=active_user, league=current_league):

                if not Team.objects.filter(name=name, league=current_league):

                    new_league_team = Team(name = name, manager = active_user, league = current_league)

                    new_league_team.slug = slugify(new_league_team.name)
                    new_league_team.save()

                    new_league_team_dict = new_league_team.to_json()

                    return JsonResponse({'Success':True, 'new_league_team_dict': new_league_team_dict})
                return JsonResponse({'Success':False, 'Error':'Team name already taken in this league.'})
            return JsonResponse({'Success':False, 'Error':'Limit one team per manager per league.'})

class UpdateTeamView(View):

    def post(self, request, league_slug, team_slug):
        if request.session.get('_auth_user_id'):
            print(request.session.get('_auth_user_id'))
            active_user_id = int(request.session.get('_auth_user_id'))
            active_user = User.objects.filter(id=active_user_id)[0]

            current_league = League.objects.filter(slug = league_slug)[0]

            print(current_league)

            current_team = Team.objects.filter(slug = team_slug, league = current_league)[0]
            print(current_team)

            if active_user == current_team.manager:

                name = request.POST['name']
                mascot = request.POST['mascot']

                if not Team.objects.filter(name=name, league=current_league):

                    current_team.name = name
                    current_team.mascot = mascot
                    current_team.slug = slugify(current_team.name)
                    current_team.save()
                    updated_team_dict = current_team.to_json()

                    return JsonResponse({'Success':True, 'updated_team_dict':updated_team_dict})
                return JsonResponse({'Success':False, 'Error':'Team name already taken in this league'})

if __name__ == '__main__':
    pal = Selection(13,'New England Patriots')
    print(pal)
