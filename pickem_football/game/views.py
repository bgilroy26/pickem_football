from django.shortcuts import render,redirect
from django.views.generic import View
from django.http import JsonResponse,Http404
from django.models import Game, WeekResults
import requests
import json
# Create your views here.
class MatchupView(View):
    url = 'http://127.0.0.1:8000/fballAPI/2014/week-1/matchups/'

    def get(self, request):
        r = requests.get(url)
        string_dict = r.content
        matchup_dict = json.loads(string_dict)
        return JsonResponse(matchup_dict)


class WeekResultsView(View):
    scores_url = 'http://127.0.0.1:8000/fballAPI/2014/week-1/scores/'

    def get(self, request):
        r = requests.get(url)
        string_dict = r.content
        scores_dict = json.loads(string_dict)
        return JsonResponse(matchup_dict)
