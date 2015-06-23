from django.conf.urls import patterns,include, url
from django.contrib import admin
from django.views.generic import View
from interface.views import IndexView, LoginView, RegisterView, LogoutView, ProfileView, TeamView, CreateLeagueView, LeagueView, CreateTeamView, TeamView, MatchupView, MakePicksView


urlpatterns = patterns('',

    url(r'^index/$', IndexView.as_view(), name = 'index'),

    url(r'^login/$', LoginView.as_view(), name = 'login'),

    url(r'^register/$', RegisterView.as_view(), name = 'register'),

    url(r'^logout/$', LogoutView.as_view(), name = 'logout'),

    url(r'^profile/(?P<username>[a-z0-9A-z+._@-]{1,30})/$', ProfileView.as_view(), name = 'profile'),

    url(r'^league/create_league/$', CreateLeagueView.as_view(), name ='create_league'),

    url(r'^league/(?P<league_slug>[a-z-]+)/$', LeagueView.as_view(), name = 'league_view'),

    url(r'^league/(?P<league_slug>[a-z-]+)/team/create_team/$', CreateTeamView.as_view(), name = 'create_team'),

    url(r'^league/(?P<league_slug>[a-z-]+)/team/(?P<team_slug>[a-z-]+)/$', TeamView.as_view(), name = 'team_view'),

    url(r'^league/(?P<league_slug>[a-z-]+)/team/(?P<team_slug>[a-z-]+)/(?P<week_slug>week-[1-9][0-7]?)/$', MatchupView.as_view(), name = 'matchups'),

    url(r'^league/(?P<league_slug>[a-z-]+)/team/(?P<team_slug>[a-z-]+)/(?P<week_slug>week-[1-9][0-7]?)/make_picks/$', MakePicksView.as_view(), name = 'make_picks'),

)
