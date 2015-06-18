from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import JsonResponse, Http404
from interface.forms import UserForm,UserProfileForm,UserExtendedProfileForm
import os
import json
import requests


class IndexView(View):
    template = 'interface/index.html'
    def get(self, request):

        r = requests.get(os.environ.get('users'))
        print(r)
        print(r.json())
        # if request.session.get('_auth_user_id'):
        #     active_user = UserMethods.objects.filter(id=_auth_user_id)[0]
        #     active_user_dict = UserMethods.objects.filter(id=_auth_user_id)[0]
        return render(request, self.template)

class LoginView(View):
    template = 'interface/login.html'
    empty_form = UserForm()

    def get(self,request):

        return render(request,self.template,{'user_form':self.empty_form})

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        payload = {'username':username, 'password':password}
        r = requests.post(os.environ.get('users') + 'login/', data = payload)
        print(r)
        if r.ok == True:
            request.session['_auth_user_id']= r.json()['_auth_user_id']
            request.session.save()
            print(request.session.get('_auth_user_id'))
            return redirect('/interface/my_page/')
        return redirect('/interface/login/')

class RegisterView(View):
    template = 'interface/register.html'
    empty_form = UserForm()

    def get(self,request):
        return render(request,self.template,{'user_form':self.empty_form})

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']

        payload = {'username':username, 'password':password}
        r = requests.post(os.environ.get('users') + 'register/', data=payload)
        if r.ok == True:
            return redirect('/interface/my_page/{}/'.format(username))
        return redirect('/interface/register/')

class LogoutView(View):
    template = 'interface/logout.html'

    def get(self,request):
        return render(request,self.template)

    def post(self,request):
        r = requests.post(os.environ.get('users') + 'logout/')
        if r.ok == True:
            return redirect('/interface/index/')
        return redirect('/interface/logout/')

class MyPageView(View):
    template = 'interface/profile.html'
    user_profile_form = UserProfileForm()
    extended_profile_form = UserExtendedProfileForm()

    def get(self,request):
        if request.session.get('_auth_user_id'):
            _auth_user_id= request.session.get('_auth_user_id')
            r = requests.get(os.environ.get('users')+str(_auth_user_id)+"/profile/")
            active_user_teams_dict = r.json()['teams']
            active_user_dict = r.json()['active_user']
            return render(request,self.template,{'active_user_teams_dict':active_user_teams_dict, 'active_user_dict':active_user_dict, 'user_profile_form': self.user_profile_form, 'extended_profile_form':extended_profile_form})
        return redirect('/interface/index/')
        # if request.session.get('_auth_user_id'):
        #     active_user_id = int(request.session.get('_auth_user_id'))
        #     active_user = User.objects.filter(id=active_user_id)[0]
        #     if User.objects.filter(username=username):
        #         profiled_user = User.objects.filter(username=username)[0]
        #         viewed_user_profile = UserProfile.objects.filter(user=profiled_user)[0]
        #         if profiled_user.id == active_user.id:
        #             profile_form = UserProfileForm(initial={'first_name':profiled_user.first_name, 'last_name':profiled_user.last_name})
        #             extended_profile_form = UserExtendedProfileForm(initial={'about':viewed_user_profile.about})
        #             viewed_user_profile.picture = viewed_user_profile.picture.name.strip('users/static/users/')
        #             viewed_user_profile.save()
        #             return render(request,self.template,{'active_user':active_user,'profile_form':profile_form, 'profiled_user':profiled_user,'viewed_user_profile':viewed_user_profile,'extended_profile_form':extended_profile_form})

    # @login_required
    # def post(self, request, username):
    #     empty_profile_form = UserProfileForm
    #     empty_extended_form = UserExtendedProfileForm
    #
    #     if request.session.get('_auth_user_id'):
    #         active_user_id = int(request.session.get('_auth_user_id'))
    #         active_user = User.objects.filter(id=active_user_id)[0]
    #         if User.objects.filter(username=username):
    #             profiled_user = User.objects.filter(username=username)[0]
    #             viewed_user_profile = UserProfile.objects.filter(user=profiled_user)[0]
    #             if active_user_id == profiled_user.id:
    #                 updated_form = UserProfileForm(request.POST)
    #                 updated_extended_form = UserExtendedProfileForm(request.POST,request.FILES)
    #                 if updated_form.is_valid() and updated_extended_form.is_valid():
    #                     profiled_user.first_name = updated_form.cleaned_data.get('first_name')
    #                     profiled_user.last_name = updated_form.cleaned_data.get('last_name')
    #                     profiled_user.save()
    #                     viewed_user_profile.about = updated_extended_form.cleaned_data.get('about')
    #                     viewed_user_profile.picture = updated_extended_form.cleaned_data.get('picture')
    #                     viewed_user_profile.save()
    #                 return redirect('/users/{}/'.format(profiled_user))
    #             return render(request, self.template, {'error':'Invalid input; please try again','user':profiled_user,'profile_form':empty_profile_form,'extended_profile_form':empty_extended_form})
    #     return redirect('/game/index/')
