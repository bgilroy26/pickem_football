from django.conf.urls import patterns,include, url
from django.contrib import admin
from django.views.generic import View
from interface.views import IndexView, LoginView, RegisterView, LogoutView, ProfileView, TeamView, CreateLeagueView, LeagueView, CreateTeamView, TeamView, MatchupView, MakePicksView,AdminMenuView, WeekView, LeagueWeekView,BaseView


urlpatterns = patterns('',

    url(r'^$', BaseView.as_view(), name = 'base'),

    url(r'^admin_menu/$', AdminMenuView.as_view(), name = 'admin_menu'),

    url(r'^(?P<week_slug>week-[1-9][0-7]?)/results/$', WeekView.as_view(), name = 'week_view'),

    url(r'^(?P<week_slug>week-[1-9][0-7]?)/results/league/(?P<league_slug>[a-z0-9-]+)/$', LeagueWeekView.as_view(), name = 'league_week_view'),

    url(r'^index/$', IndexView.as_view(), name = 'index'),

    url(r'^login/$', LoginView.as_view(), name = 'login'),

    url(r'^register/$', RegisterView.as_view(), name = 'register'),

    url(r'^logout/$', LogoutView.as_view(), name = 'logout'),

    url(r'^profile/(?P<username>[a-z0-9A-z+._@-]{1,30})/$', ProfileView.as_view(), name = 'profile'),

    url(r'^league/create_league/$', CreateLeagueView.as_view(), name ='create_league'),

    url(r'^league/(?P<league_slug>[a-z0-9-]+)/$', LeagueView.as_view(), name = 'league_view'),

    url(r'^league/(?P<league_slug>[a-z0-9-]+)/team/create_team/$', CreateTeamView.as_view(), name = 'create_team'),

    url(r'^league/(?P<league_slug>[a-z0-9-]+)/team/(?P<team_slug>[a-z-]+)/$', TeamView.as_view(), name = 'team_view'),

    url(r'^league/(?P<league_slug>[a-z0-9-]+)/team/(?P<team_slug>[a-z-]+)/(?P<week_slug>week-[1-9][0-7]?)/$', MatchupView.as_view(), name = 'matchups'),

    url(r'^league/(?P<league_slug>[a-z0-9-]+)/team/(?P<team_slug>[a-z-]+)/(?P<week_slug>week-[1-9][0-7]?)/make_picks/$', MakePicksView.as_view(), name = 'make_picks'),

)
