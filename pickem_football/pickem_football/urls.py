from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

url(r'^game/', include('game.urls', namespace = 'game', app_name = 'game')),

url(r'^admin/', include(admin.site.urls)),

url(r'', include('interface.urls', namespace = 'interface', app_name = 'interface')),
)
