from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

url(r'^interface/', include('interface.urls')),

url(r'^game/', include('game.urls')),

url(r'^users/', include('users.urls')),

url(r'^admin/', include(admin.site.urls)),

)
