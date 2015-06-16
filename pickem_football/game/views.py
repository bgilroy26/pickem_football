from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import JsonResponse,Http404
from game.models import League, Team, TeamPick
from users.models import User
from game.services import get_weekly_record
import requests
import json
import os

class ActiveTeamsView(View):

	def get(self,request,username):
		player_teams = Team.objects.filter(user__username=username,league__nfl_year=2014)
		return JsonResponse({'active_player_teams':player_teams})

class PastTeamsView(View):

	def get(self,request,username):
		player_teams = Team.objects.filter(user__username=username,league__nfl_year=year).exclude(league__nfl_year=2014)
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
		if request.session.get('_auth_user_id'):
			active_user_id = int(request.session.get('_auth_user_id'))
			active_user = User.objects.filter(id=active_user_id)[0]
			week_int = int(week.strip('week-'))

			r = requests.get(os.environ.get('fballAPI') + year + '/' + week + '/matchups/')

			string_dict = r.content.decode("utf-8")
			matchups_dict = json.loads(string_dict)

			current_team = Team.objects.filter(slug=team_slug)[0]
			team_dict = current_team.to_json()
			team_picks = TeamPick.objects.filter(team = current_team, nfl_week = week_int)

			pick_dict = {'{}\'s_{}_picks'.format(current_team.name, week):[pick.to_json() for pick in team_picks]}

			return JsonResponse({'team_dict':team_dict, 'matchups_dict':matchups_dict, 'weekly_picks':pick_dict})

	def post(self, request, year, week, team_slug):

			choice = request.POST['choice']
			week_int = int(week.strip('week-'))

			current_team = Team.objects.filter(slug=team_slug)[0]
			team_dict = current_team.to_json()
			new_pick = TeamPick.objects.update_or_create(choice = choice, team = current_team, nfl_week=week_int)[0]
			new_pick_dict = new_pick.to_json()

			return redirect('/game/{}/{}/{}/enter_pick/'.format(year,week,team_slug))

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
			print(current_team.wins)
			print(current_team.losses)
			team_picks_list = TeamPick.objects.filter(team=current_team,nfl_week=week_int)


			pick_list_dict = {'weekly_picks': [pick.choice for pick in team_picks_list]}

			winning_teams_list = winners_dict['winning_teams']

			for nfl_team_pick in team_picks_list:
				if TeamPick.objects.filter(team=current_team, nfl_week=week_int, choice = nfl_team_pick, was_counted=False):
					if nfl_team_pick.choice in winning_teams_list:
						nfl_team_pick.correct = True

					nfl_team_pick.was_counted = True
					nfl_team_pick.save()

			team_dict = current_team.to_json()

			current_team_weekly_record_dict = get_weekly_record(week_int,current_team)

			return JsonResponse({'current_team_weekly_record_dict':current_team_weekly_record_dict, 'team_dict':team_dict, 'winners_dict': winners_dict,'pick_list_dict':pick_list_dict})
