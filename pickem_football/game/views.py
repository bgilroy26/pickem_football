from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import JsonResponse,Http404
from game.models import League, Team, TeamPick
from users.models import User
import requests
import json
# Create your views here.

class IndexView(View):
	template = 'game/index.html'

	def get(self,request):
		if request.session.get('id'):
			active_user_id = request.session.get('id')
			if User.objects.filter(id=active_user_id):
				active_user = User.objects.filter(id=active_user_id)[0]
				if Membership.objects.filter(user=active_user):
					user_teams = Team.objects.filter(user=active_user)
					for team in user_teams:
						# if League.objects.filter(team=team):
						# 	all_leagues = League.objects.filter(membership=a_membership)
							return render(request,self.template,{'active_user':active_user})
		return render(request, self.template)

class LeagueView(View):
	template = 'game/user_leagues.html'

	def get(self,request):
		if request.session.get('id'):
			active_user_id = request.session.get('id')
			if User.objects.filter(id=active_user_id):
				active_user = User.objects.filter(id=active_user_id)[0]
				if Membership.objects.filter(user=active_user):
					user_memberships = Membership.objects.filter(user=active_user)
					for a_membership in user_memberships:
						if League.objects.filter(membership=a_membership):
							all_leagues = League.objects.filter(membership=a_membership)
							return render(request,self.template, {'active_user':active_user, 'user_leagues': user_leagues, 'user_memberships':user_memberships})
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
