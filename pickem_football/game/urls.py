from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import View
from game.views import ActiveTeamsView,PastTeamsView,InvitesView,WeeklyMatchupsView,WeeklyScoresView,TeamPickView,WeeklyTeamResultsView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',

    url(r'^(?P<username>[a-z0-9A-Z]{1,20})/$', ActiveTeamsView.as_view()),

    url(r'^(?P<username>[a-z0-9A-Z]{1,20})/$', PastTeamsView.as_view()),

    url(r'^(?P<year>20[0-2][0-9])/(?P<week>week-{1}[1]*[0]*[0-7]{1})/matchups/$', WeeklyMatchupsView.as_view()),

    url(r'^(?P<year>20[0-2][0-9])/(?P<week>week-{1}[1]*[0]*[0-7]{1})/results/$', WeeklyScoresView.as_view()),

    url(r'^(?P<year>20[0-2][0-9])/(?P<week>week-{1}[1]*[0]*[0-7]{1})/(?P<team_slug>[a-z-]+)/enter_pick/$', csrf_exempt(TeamPickView.as_view())),

    url(r'^(?P<year>20[0-2][0-9])/(?P<week>week-{1}[1]*[0]*[0-7]{1})/(?P<team_slug>[a-z-]+)/results/$', csrf_exempt(WeeklyTeamResultsView.as_view())),
)
