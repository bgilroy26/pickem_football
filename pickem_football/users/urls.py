from django.conf.urls import include, url,patterns
from django.contrib import admin
from users.views import RegisterView,LoginView, ProfileView, LogoutView
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt


urlpatterns = patterns('',

    # url(r'^index$',IndexView.as_view()),

    url(r'^login/$', csrf_exempt(LoginView.as_view())),

    url(r'^register/$', csrf_exempt(RegisterView.as_view())),

    url(r'^logout/$', csrf_exempt(LogoutView.as_view())),

    url(r'^(?P<username>[a-z0-9A-Z]{1,20})/$', csrf_exempt(ProfileView.as_view())),

    # url(r'^search$', SearchView.as_view()),
    #
    # url(r'^post$', PostView.as_view()),
    #
    # url(r'^repost$', RepostView.as_view()),
)
