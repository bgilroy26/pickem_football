from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import View
from game.views import MatchupView
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pickem_football.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^matchups/$', include('game.urls')),

)
