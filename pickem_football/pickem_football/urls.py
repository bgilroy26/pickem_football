from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

url(r'^interface/', include('interface.urls', namespace = 'interface', app_name = 'interface')),

url(r'^game/', include('game.urls', namespace = 'game', app_name = 'game')),

url(r'^admin/', include(admin.site.urls)),

)
