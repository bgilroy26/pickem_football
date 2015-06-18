from django.shortcuts import render,redirect
from users.forms import UserForm,UserProfileForm, UserExtendedProfileForm
from users.models import User,UserProfile
from game.models import League, Team, TeamPick
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import JsonResponse,Http404
from django.contrib.auth.decorators import login_required
import json
import requests


class LoginView(View):
    template = 'users/login.html'
    empty_form = UserForm()

    def get(self,request):
        if request.session.get('_auth_user_id'):
            active_user_id = int(request.session.get('_auth_user_id'))
            if User.objects.filter(id=active_user_id):
                active_user = User.objects.filter(id=active_user_id)[0]
        #         return JsonResponse({'user_form':self.empty_form, 'active_user', active_user})
        # return JsonResponse({'Error':'Login Error, try again', 'user_form': self.empty_form, 'active_user':active_user})
                return render(request,self.template,{'user_form':self.empty_form, 'active_user':active_user})
        return render(request,self.template,{'user_form':self.empty_form})

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        active_user = authenticate(username=username, password=password)
        if active_user:
            login(request,active_user)
            return redirect('/users/{}/'.format(active_user.username))
        return render(request, self.template, {'error':'Name and/or password incorrect.  Please try again.', 'user_form':self.empty_form})

class RegisterView(View):
    empty_form = UserForm()
    template = 'users/register.html'

    def get(self,request):
        if request.session.get('_auth_user_id'):
            active_user_id = int(request.session.get('_auth_user_id'))
            if User.objects.filter(id=active_user_id):
                active_user = User.objects.filter(id=active_user_id)[0]
                return render(request,self.template,{'user_form':self.empty_form,'active_user':active_user})
        return render(request,self.template,{'user_form':self.empty_form})

    def post(self,request):
        submitted_form = UserForm(request.POST)
        if request.session.get('_auth_user_id'):
            active_user_id = int(request.session.get('_auth_user_id'))
            if submitted_form.is_valid():
                username = submitted_form.cleaned_data.get('username')
                submitted_password = submitted_form.cleaned_data.get('password')
                new_user = User.objects.create_user(username = username, password = submitted_password)
                new_user_profile = UserProfile(user=new_user)
                new_user_profile.save()
                authorized_user = authenticate(username=username,password=submitted_password)
                login(request,authorized_user)
                return redirect('/users/{}/'.format(authorized_user.username))
            return render(request,self.template,{'error':'Invalid input, please try again', 'user_form':self.empty_form})

class LogoutView(View):
    template = 'users/logout.html'

    def get(self,request):
        if request.session.get('_auth_user_id'):
            active_user_id = int(request.session.get('_auth_user_id'))
            if User.objects.filter(id=active_user_id):
                active_user = User.objects.filter(id=active_user_id)[0]
                return render(request,self.template,{'active_user':active_user})
        return redirect('/game/index/')

    def post(self,request):
        logout(request)
        return redirect('/game/index/')

class ProfileView(View):
    template = 'users/profile.html'
        #@login_required
    def get(self,request,username):
        if request.session.get('_auth_user_id'):
            active_user_id = int(request.session.get('_auth_user_id'))
            active_user = User.objects.filter(id=active_user_id)[0]
            if User.objects.filter(username=username):
                profiled_user = User.objects.filter(username=username)[0]
                viewed_user_profile = UserProfile.objects.filter(user=profiled_user)[0]
                if profiled_user.id == active_user.id:
                    profile_form = UserProfileForm(initial={'first_name':profiled_user.first_name, 'last_name':profiled_user.last_name})
                    extended_profile_form = UserExtendedProfileForm(initial={'about':viewed_user_profile.about})
                    viewed_user_profile.picture = viewed_user_profile.picture.name.strip('users/static/users/')
                    viewed_user_profile.save()
                    return render(request,self.template,{'active_user':active_user,'profile_form':profile_form, 'profiled_user':profiled_user,'viewed_user_profile':viewed_user_profile,'extended_profile_form':extended_profile_form})
                return render(request,self.template,{'active_user':active_user,'profiled_user':profiled_user})
            return redirect('/game/index/')

    # @login_required
    def post(self, request, username):
        empty_profile_form = UserProfileForm
        empty_extended_form = UserExtendedProfileForm
        if request.session.get('_auth_user_id'):
            active_user_id = int(request.session.get('_auth_user_id'))
            active_user = User.objects.filter(id=active_user_id)[0]
            if User.objects.filter(username=username):
                profiled_user = User.objects.filter(username=username)[0]
                viewed_user_profile = UserProfile.objects.filter(user=profiled_user)[0]
                if active_user_id == profiled_user.id:
                    updated_form = UserProfileForm(request.POST)
                    updated_extended_form = UserExtendedProfileForm(request.POST,request.FILES)
                    if updated_form.is_valid() and updated_extended_form.is_valid():
                        profiled_user.first_name = updated_form.cleaned_data.get('first_name')
                        profiled_user.last_name = updated_form.cleaned_data.get('last_name')
                        profiled_user.save()
                        viewed_user_profile.about = updated_extended_form.cleaned_data.get('about')
                        viewed_user_profile.picture = updated_extended_form.cleaned_data.get('picture')
                        viewed_user_profile.save()
                    return redirect('/users/{}/'.format(profiled_user))
                return render(request, self.template, {'error':'Invalid input; please try again','user':profiled_user,'profile_form':empty_profile_form,'extended_profile_form':empty_extended_form})
        return redirect('/game/index/')
