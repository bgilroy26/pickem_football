from django.conf.urls import patterns,include, url
from django.contrib import admin
from django.views.generic import View
from interface.views import IndexView, LoginView,RegisterView,LogoutView, MyPageView


urlpatterns = patterns('',

    url(r'^index/$', IndexView.as_view()),

    url(r'^login/$', LoginView.as_view()),

    url(r'^register/$', RegisterView.as_view()),

    url(r'^logout/$', LogoutView.as_view()),

    url(r'^my_page/$', MyPageView.as_view()),

)
