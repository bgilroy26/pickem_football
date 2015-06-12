from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import View
from game.views import IndexView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pickem_football.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^index/$' IndexView.as_view()),

    url(r'^(?P<username>[a-z0-9A-Z]{1,20})/$', ActiveTeamView.as_view()),

    url(r'^(?P<username>[a-z0-9A-Z]{1,20})/$', PastTeamView.as_view()),

    
)
