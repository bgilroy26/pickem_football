from django.views.generic import View
from django.http import JsonResponse,Http404
from game.models import League, Team, TeamPick
from users.models import User
import requests
import json

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


class LeagueView(View):

	def get(self,request):
		if request.session.get('_auth_user_id'):
			active_user_id = int(request.session.get('_auth_user_id'))
			if User.objects.filter(id=active_user_id):
				active_user = User.objects.filter(id=active_user_id)[0]
				# if Membership.objects.filter(user=active_user):
					# user_memberships = Membership.objects.filter(user=active_user)
					# for a_membership in user_memberships:
						# if League.objects.filter(membership=a_membership):
							# all_leagues = League.objects.filter(membership=a_membership)
				return render(request,self.template, {'active_user':active_user, 'user_leagues': user_leagues})
		return render(request, self.template)

# class MatchupView(View):
# 	url = 'http://127.0.0.1:8000/fballAPI/'
#
# 	def get(self, request, year, week):
# 		r = requests.get(url)
# 		string_dict = r.content
# 		matchup_dict = json.loads(string_dict)
# 		return JsonResponse(matchup_dict)
#
#
# class WeekResultsView(View):
#     scores_url = 'http://127.0.0.1:8000/fballAPI/2014/week-1/scores/'
#
#     def get(self, request):
#         r = requests.get(url)
#         string_dict = r.content
#         scores_dict = json.loads(string_dict)
#         return JsonResponse(matchup_dict)
