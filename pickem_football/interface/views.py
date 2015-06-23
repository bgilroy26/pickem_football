from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from users.forms import UserForm,UserProfileForm,UserExtendedProfileForm
from users.models import User, UserProfile
from game.models import Team, League, TeamPick
from game.forms import LeagueForm, TeamForm
from django.utils.text import slugify
from django import forms
import os
import requests
import json


class IndexView(View):
    template = 'interface/index.html'

    def get(self, request):

        if not request.user.is_anonymous():
            active_user = User.objects.filter(id=request.user.id)[0]
            all_users = User.objects.all()
            all_leagues = League.objects.all()
            return render(request, self.template,{'active_user':active_user,'all_users':all_users,'all_leagues':all_leagues})
        return render(request, self.template)

class LoginView(View):
    template = 'interface/login.html'
    login_form = UserForm()

    def get(self,request):
        if not request.user.is_anonymous():
            active_user = User.objects.filter(id = request.user.id)[0]
            return render(request,self.template,{'user_form':self.login_form,'active_user':active_user})
        return render(request,self.template,{'user_form':self.login_form})


    def post(self,request):
        submitted_form = UserForm(request.POST)
        username = submitted_form._raw_value('username')
        password = submitted_form._raw_value('password')
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user:
            login(request,authenticated_user)
            auth_user = User.objects.filter(username=authenticated_user)[0]
            return redirect('interface:profile', username = auth_user.username)
        return redirect('interface:login')

class RegisterView(View):
    template = 'interface/register.html'
    register_form = UserForm()

    def get(self,request):
        if not request.user.is_anonymous():
            active_user = User.objects.filter(id = request.user.id)[0]
            return render(request,self.template,{'register_form':self.register_form,'active_user':active_user})
        return render(request,self.template,{'register_form':self.register_form})

    def post(self,request):
        submitted_form = UserForm(request.POST)
        if submitted_form.is_valid():
            submitted_username = submitted_form.cleaned_data.get('username')
            submitted_password = submitted_form.cleaned_data.get('password')
            new_user = User.objects.create_user(username = submitted_username, password = submitted_password)
            if new_user:
                new_user_profile = UserProfile(user=new_user)
                new_user_profile.save()
                authenticated_user = authenticate(username=submitted_username,password=submitted_password)
                login(request,authenticated_user)
                return redirect('interface:profile', username = new_user.username)
        return redirect('interface:register')

class LogoutView(View):
    template = 'interface/logout.html'

    def get(self,request):
        if not request.user.is_anonymous():
            active_user = User.objects.filter(id = request.user.id)[0]
            return render(request,self.template,{'active_user':active_user})
        return redirect('interface:index')

    def post(self,request):
        logout(request)
        return redirect('interface:index')

class ProfileView(View):
    template = 'interface/profile.html'

    def get(self,request,username):
        if not request.user.is_anonymous():
            active_user = User.objects.filter(id = request.user.id)[0]
            if User.objects.filter(username=username):
                profiled_user = User.objects.filter(username=username)[0]
                viewed_user_profile = UserProfile.objects.filter(user=profiled_user)[0]
                viewed_user_profile.picture = viewed_user_profile.picture.name.strip('users/static/users/')
                viewed_user_profile.save()
                user_teams = Team.objects.filter(manager = profiled_user)
                if active_user == profiled_user:
                    user_profile_form = UserProfileForm(initial={'first_name':profiled_user.first_name, 'last_name':profiled_user.last_name,'email':profiled_user.email})
                    extended_profile_form = UserExtendedProfileForm(initial={'about':viewed_user_profile.about,'picture':viewed_user_profile.picture})
                    return render(request,self.template,{'active_user':active_user, 'user_profile_form': user_profile_form,
                    'extended_profile_form':extended_profile_form,'profiled_user':profiled_user,'viewed_user_profile':viewed_user_profile,'user_teams':user_teams})
                return render(request, self.template,{'active_user':active_user,'profiled_user':profiled_user,'viewed_user_profile':viewed_user_profile,'user_teams':user_teams})
            return redirect('interface:index')
        return redirect('interface:index')

    def post(self, request, username):
        if not request.user.is_anonymous():
            active_user_id = request.user.id
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
                        profiled_user.email = updated_form.cleaned_data.get('email')
                        profiled_user.save()
                        viewed_user_profile.about = updated_extended_form.cleaned_data.get('about')
                        viewed_user_profile.picture = updated_extended_form.cleaned_data.get('picture')
                        if viewed_user_profile.picture is not None:
                            viewed_user_profile.picture = updated_extended_form.cleaned_data.get('picture')
                        viewed_user_profile.save()
                        return redirect('interface:profile', username = profiled_user.username)
            return redirect('interface:profile', username = profiled_user.username)
        return redirect('interface:login')

class CreateLeagueView(View):
    template = 'interface/create_league.html'
    league_form = LeagueForm()

    def get(self, request):
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            return render(request, self.template, {'active_user':active_user, 'league_form':self.league_form})
        return redirect('interface:login')

    def post(self, request):
        if not request.user.is_anonymous():
            league_form = LeagueForm(request.POST,request.FILES)
            marquee = league_form.files.get('marquee')
            name = league_form.data.get('name')
            buy_in = league_form.data.get('buy_in')
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]

            new_league = League(name=name, buy_in = buy_in, commissioner = active_user)
            new_league.slug = slugify(new_league.name)
            new_league.save()
            if new_league:
                return redirect('interface:league_view', league_slug = new_league.slug)
            return redirect('interface:create_league')
        return redirect('interface:login')

class LeagueView(View):
    template = 'interface/leagueview.html'

    def get(self, request, league_slug):
        league_form = LeagueForm()
        league_form.fields['name'].widget=forms.HiddenInput()
        league_form.fields['buy_in'].widget=forms.HiddenInput()
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug=league_slug)[0]
            league_teams = Team.objects.filter(league=current_league).order_by('-wins')
            if active_user == current_league.commissioner:

                current_league.marquee = current_league.marquee.name.strip('/game/static/league/')
                current_league.save()
                return render(request, self.template, {'active_user':active_user, 'current_league':current_league, 'league_teams':league_teams, 'league_form':league_form})
            return render(request, self.template, {'active_user':active_user, 'current_league':current_league, 'league_teams':league_teams})
        return redirect('interface:login')

    def post(self,request,league_slug):

        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug=league_slug)[0]

            if active_user == current_league.commissioner:
                league_form = LeagueForm(request.POST,request.FILES)
                marquee = league_form.files.get('marquee')
                if marquee is not None:
                    current_league.marquee = marquee

                current_league.save()

            return redirect('interface:league_view', league_slug = current_league.slug)
        return redirect('interface:login')

class CreateTeamView(View):
    template = 'interface/create_team.html'
    team_form = TeamForm()

    def get(self, request, league_slug):
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug = league_slug)[0]
            return render(request, self.template, {'active_user':active_user, 'current_league':current_league, 'team_form':self.team_form})
        return redirect('interface:login')

    def post(self, request, league_slug):
        print('hellloooo')
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug=league_slug)[0]
            print('howyza')
            name = request.POST['name']
            print('howdy')
            if not Team.objects.filter(manager=active_user, league=current_league):
                print('hi')

                if not Team.objects.filter(name=name, league=current_league):
                    print('hey')

                    new_league_team = Team(name = name, manager = active_user, league = current_league)

                    new_league_team.slug = slugify(new_league_team.name)
                    new_league_team.save()

                    return redirect('interface:team_view', league_slug = current_league.slug, team_slug = new_league_team.slug)
                return redirect('interface:create_team', league_slug = current_league.slug)
        return redirect('interface:index')

class TeamView(View):
    template = 'interface/teamview.html'
    def get(self,request, league_slug, team_slug):
        team_form = TeamForm()
        team_form.fields['name'].widget=forms.HiddenInput()

        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug=league_slug)[0]
            current_team = Team.objects.filter(slug=team_slug)[0]
            week_list = []
            for x in range(1,18):
                week_list.append({'slug':"week-"+str(x),'week':x})

            if active_user == current_team.manager:
                # team_form = TeamForm(initial={'name':current_team.name})
                current_team.name = current_team.name
                current_team.mascot = current_team.mascot.name.strip('game/static/team/')
                current_team.slug = slugify(current_team.name)
                current_team.save()
                return render(request, self.template, {'active_user':active_user, 'current_team':current_team, 'team_form':team_form, 'current_league':current_league, 'week_list':week_list})
            return render(request, self.template, {'active_user':active_user, 'current_team':current_team,'current_league':current_league,'week_list':week_list})
        return redirect('interface:login')

    def post(self, request, league_slug, team_slug):
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]

            current_league = League.objects.filter(slug = league_slug)[0]

            current_team = Team.objects.filter(slug = team_slug, league = current_league)[0]

            if active_user == current_team.manager:
                team_form = TeamForm(request.POST,request.FILES)
                mascot = team_form.files.get('mascot')
                name = team_form.data.get('name')

                if name != current_team.name:

                    if not Team.objects.filter(name=name, league=current_league):

                        current_team.name = name
                        current_team.slug = slugify(current_team.name)

                if mascot is not None:
                    current_team.mascot = mascot

                current_team.save()

                return redirect('interface:team_view', league_slug = league_slug, team_slug = team_slug)
        return redirect('interface:login')

class MatchupView(View):
    template = 'interface/matchup.html'

    def get(self, request, league_slug, team_slug, week_slug):
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]

            current_league = League.objects.filter(slug = league_slug)[0]
            print(week_slug)
            current_team = Team.objects.filter(slug = team_slug, league = current_league)[0]
            week = week_slug.strip('week-')
            r = requests.get(os.environ.get('fballAPI') + week_slug + '/matchups/')
            matchup_list = r.json()['week_{}_schedule'.format(week)]
            print('matchup_list')
            print(matchup_list)

            current_picks = TeamPick.objects.filter(team=current_team, nfl_week=int(week))
            current_picks_dict_list = [pick.to_json() for pick in current_picks]

            #for pick in current_picks_dict_list:
                # pick["updated_at"] = pick['updated_at'].isoformat()
                # pick["created_at"] = pick['created_at'].isoformat()

            json_data = {'picks': current_picks_dict_list}

            matchup_id = -1
            for game in matchup_list:
                matchup_id += 1

                game['id'] = matchup_id

            return render(request, self.template, {'current_league':current_league, 'current_team':current_team, 'matchup_list':matchup_list, 'active_user':active_user,'json_data':json_data, 'week':week, 'week_slug':week_slug})
        return redirect('interface:login')

class MakePicksView(View):
    def post(self, request, league_slug, team_slug, week_slug):
        pass
