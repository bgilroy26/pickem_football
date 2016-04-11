from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View, RedirectView
from users.forms import UserForm,UserProfileForm,UserExtendedProfileForm
from users.models import User, UserProfile
from game.models import Team, League, TeamPick
from game.forms import LeagueForm, TeamForm
from django.utils.text import slugify
from django import forms
from game.services import get_weekly_record, tally_weekly_results
import os
import requests
import json

# class BaseView(View):
#     def get(self, request):
#         return redirect('interface:index')

class BaseRedirectView(RedirectView):
    def get(self, request, *args, **kwargs):
        self.url = '/index/'
        self.permanent = True
        return super().get(request, *args, **kwargs)

class IndexView(View):
    template = 'interface/index.html'

    def get(self, request):
        all_users = User.objects.all()
        all_leagues = League.objects.all()
        all_teams = Team.objects.all().order_by('-wins')
        week_list = [{'slug':"week-"+str(x),'week':x} for x in range(1,18)]
        week_slug_list = ["week-"+str(x) for x in range(1,18)]
        team_record_list = []
        for team in all_teams:
            team_win_count = len(TeamPick.objects.filter(team=team, correct=True))
            team_record_list.append((team, str(team_win_count) + ' - ' + str(team.losses)))
        if request.user.is_superuser:
            superuser = User.objects.filter(id=request.user.id)[0]
            return render(request, self.template,{'team_record_list':team_record_list,'superuser':superuser,'all_users':all_users,'all_leagues':all_leagues,'week_list':week_list,'week_slug_list':week_slug_list})
        if not request.user.is_anonymous():
            active_user = User.objects.filter(id=request.user.id)[0]
            return render(request, self.template,{'team_record_list':team_record_list,'active_user':active_user,'all_users':all_users,'all_leagues':all_leagues,'all_teams':all_teams, 'week_list':week_list,'week_slug_list':week_slug_list})
        return render(request, self.template)


class LoginView(View):
    template = 'interface/login.html'
    login_form = UserForm()

    def get(self,request):
        if request.user.is_superuser:
            superuser = User.objects.filter(id=request.user.id)[0]
            return render(request, self.template,{'superuser':superuser,'user_form':self.login_form,})
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
        if request.user.is_superuser:
            superuser = User.objects.filter(id=request.user.id)[0]
            return render(request,self.template,{'superuser':superuser,'user_form':self.register_form,'active_user':active_user})
        if not request.user.is_anonymous():
            active_user = User.objects.filter(id = request.user.id)[0]
            return render(request,self.template,{'user_form':self.register_form,'active_user':active_user})
        return render(request,self.template,{'user_form':self.register_form})

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
        if request.user.is_superuser:
            superuser = User.objects.filter(id=request.user.id)[0]
            return render(request,self.template,{'superuser':superuser})
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
                viewed_user_profile.picture = viewed_user_profile.picture.name.replace('game/static/users/','')
                viewed_user_profile.save()
                user_teams = Team.objects.filter(manager = profiled_user)
                if active_user == profiled_user:
                    user_profile_form = UserProfileForm(initial={'first_name':profiled_user.first_name, 'last_name':profiled_user.last_name,'email':profiled_user.email})
                    extended_profile_form = UserExtendedProfileForm(initial={'about':viewed_user_profile.about,'picture':viewed_user_profile.picture})
                    if request.user.is_superuser:
                        superuser = active_user
                        return render(request,self.template,{'active_user':active_user,'superuser':superuser, 'user_profile_form': user_profile_form,
                    'extended_profile_form':extended_profile_form,'profiled_user':profiled_user,'viewed_user_profile':viewed_user_profile,'user_teams':user_teams})
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
                        if updated_extended_form.cleaned_data.get('picture') is not None:
                            viewed_user_profile.picture = updated_extended_form.cleaned_data.get('picture')
                        viewed_user_profile.save()
                        return redirect('interface:profile', username = profiled_user.username)
            return redirect('interface:profile', username = profiled_user.username)
        return redirect('interface:login')

class CreateLeagueView(View):
    template = 'interface/create_league.html'
    league_form = LeagueForm()

    def get(self, request):
        if request.user.is_superuser:
            superuser = User.objects.filter(id=request.user.id)[0]
            return render(request, self.template, {'superuser':superuser, 'league_form':self.league_form})
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            return render(request, self.template, {'active_user':active_user, 'league_form':self.league_form})
        return redirect('interface:login')

    def post(self, request):
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            league_form = LeagueForm(request.POST,request.FILES)
            if league_form.is_valid():
                name = league_form.data.get('name')
                buy_in = league_form.data.get('buy_in')
                active_user = User.objects.filter(id=active_user_id)[0]
                if league_form.files.get('marquee'):
                    marquee = league_form.files.get('marquee')
                    new_league = League(name=name, buy_in = buy_in, commissioner = active_user, marquee=marquee)
                else:
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
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug=league_slug)[0]
            if Team.objects.filter(league=current_league):
                league_teams = Team.objects.filter(league=current_league).order_by('-wins')
            else:
                league_teams=None
            week_list = [{'slug':"week-"+str(x),'week':x} for x in range(1,18)]

            if active_user == current_league.commissioner:
                league_form = LeagueForm(initial={'name':current_league.name, 'buy_in':current_league.buy_in, 'marquee':current_league.marquee})
                league_form.fields['buy_in'].widget=forms.HiddenInput()
                current_league.marquee = current_league.marquee.name.replace('game/static/league/','')
                current_league.save()
                if league_teams:

                    for team in league_teams:
                        if Team.objects.filter(name=team.name,manager=active_user):
                            active_user_team_in_league = Team.objects.filter(name=team.name,manager=active_user)[0]
                            return render(request, self.template, {'active_user_team_in_league':active_user_team_in_league,'active_user':active_user, 'current_league':current_league, 'league_teams':league_teams, 'league_form':league_form,'week_list':week_list})
                        return render(request, self.template, {'active_user':active_user, 'current_league':current_league, 'league_teams':league_teams, 'league_form':league_form,'week_list':week_list})
                else:
                    return render(request, self.template, {'active_user':active_user, 'current_league':current_league,'league_form':league_form})

            else:
                if league_teams:
                    for team in league_teams:
                        if Team.objects.filter(name=team.name,manager=active_user):
                            active_user_team_in_league = Team.objects.filter(name=team.name,manager=active_user)[0]
                            return render(request, self.template, {'active_user_team_in_league':active_user_team_in_league,'active_user':active_user, 'current_league':current_league, 'league_teams':league_teams,'week_list':week_list})
                        return render(request, self.template, {'active_user':active_user, 'current_league':current_league, 'league_teams':league_teams,'week_list':week_list})
                else:
                    return render(request, self.template, {'active_user':active_user, 'current_league':current_league})
        return redirect('interface:login')

    def post(self,request,league_slug):

        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug=league_slug)[0]

            if active_user == current_league.commissioner:
                submitted_form = LeagueForm(request.POST,request.FILES)
                name = submitted_form.data.get('name')
                marquee = submitted_form.files.get('marquee')

                if marquee is not None:
                    current_league.marquee = marquee

                current_league.name = name
                current_league.slug = slugify(name)
                current_league.save()

                return redirect('interface:index')
            return redirect('interface:league_view', league_slug=current_league.slug)
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
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug=league_slug)[0]
            submitted_form = TeamForm(request.POST)
            if submitted_form.is_valid:
                name = submitted_form.data.get('name')

                if not Team.objects.filter(manager=active_user, league=current_league):

                    if not Team.objects.filter(name=name, league=current_league):

                        if submitted_form.files.get('mascot'):
                            mascot = submitted_form.files.get('mascot')
                            new_league_team = Team(name = name, manager = active_user, league = current_league, mascot=mascot)
                        else:
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

        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug=league_slug)[0]
            current_team = Team.objects.filter(slug=team_slug)[0]
            week_list = [{'slug':"week-"+str(x),'week':x} for x in range(1,18)]

            if active_user == current_team.manager:
                team_form = TeamForm(initial={'name':current_team.name, 'mascot':current_team.mascot})
                current_team.name = current_team.name
                current_team.mascot = current_team.mascot.name.replace('game/static/team/','')
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
                submitted_form = TeamForm(request.POST,request.FILES)
                mascot = submitted_form.files.get('mascot')
                name = submitted_form.data.get('name')

                if mascot is not None:
                    current_team.mascot = mascot

                if name != current_team.name:

                    if not Team.objects.filter(name=name, league=current_league):

                        if not name:
                            current_team.save()
                            return redirect('interface:team_view', league_slug = league_slug, team_slug = team_slug)

                current_team.name = name
                current_team.slug = slugify(current_team.name)
                current_team.save()

                return redirect('interface:league_view', league_slug = current_league.slug)
            return redirect('interface:team_view', league_slug = current_league.slug,team_slug=current_team.slug)
        return redirect('interface:login')

class MatchupView(View):
    template = 'interface/matchup.html'

    def get(self, request, league_slug, team_slug, week_slug):
        if not request.user.is_anonymous():
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug = league_slug)[0]
            current_team = Team.objects.filter(slug = team_slug, league = current_league)[0]
            week = int(week_slug.strip('week-'))

            r = requests.get(os.environ.get('fballAPI') + week_slug + '/matchups/')
            matchup_list = r.json()['week_{}_schedule'.format(week)]
            print(matchup_list)
            if active_user == current_team.manager:
                current_picks = TeamPick.objects.filter(team=current_team, nfl_week=week)
                current_picks_dict_list = [pick.to_json() for pick in current_picks]
                json_data = {'picks': current_picks_dict_list}
                print(json_data)
                matchup_id = -1
                for game in matchup_list:
                    matchup_id += 1
                    game['id'] = matchup_id

                return render(request, self.template, {'current_league':current_league, 'current_team':current_team, 'matchup_list':matchup_list, 'active_user':active_user,'json_data':json_data, 'week':week, 'week_slug':week_slug})
            return render(request, self.template, {'current_league':current_league, 'current_team':current_team, 'matchup_list':matchup_list, 'active_user':active_user,'week_slug':week_slug, 'week':week})
        return redirect('interface:login')

class MakePicksView(View):
    def post(self, request, league_slug, team_slug, week_slug):
        pass

class AdminMenuView(View):
    template = 'interface/admin.html'

    def get(self, request):
        if request.user.is_superuser:
            superuser = User.objects.filter(id=request.user.id)[0]
            return render(request, self.template,{'superuser':superuser})
        return redirect('interface:index')

    def post(self, request):
        week_to_complete = request.POST.get('week')
        week_slug = 'week-{}'.format(week_to_complete)
        week = int(week_slug.strip('week-'))
        r = requests.get(os.environ.get('fballAPI') + week_slug + '/matchups/')
        winners_list = r.json().get('winning_teams')
        all_teams = Team.objects.all()
        for team in all_teams:
            get_weekly_record(int(week_to_complete), team)
            pick_list_dict = tally_weekly_results(int(week_to_complete), team, winners_list)
        return redirect('interface:week_view', week_slug=week_slug)

class WeekView(View):
    template = 'interface/results.html'

    def get(self, request, week_slug):
        if not request.user.is_anonymous():
            week = int(week_slug.strip('week-'))
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            r = requests.get(os.environ.get('fballAPI') + week_slug + '/winners/')
            all_teams = Team.objects.all()
            # game_count = len(winners_list)
            winners_list = r.json().get('winning_teams')
            try:
                game_count = r.json().get('game_count')
            except ValueError:
                game_count = 0
            team_weekly_record_list = []
            for team in all_teams:
                # picks_by_team_by_week = TeamPick.objects.filter(nfl_week=week, team=team, correct=True)
                team_win_count = len(TeamPick.objects.filter(team=team, nfl_week=week, correct=True))
                team_weekly_record_list.append((team, str(team_win_count) + ' - ' + str(game_count - team_win_count)))
                # team_weekly_record_list = team_weekly_record_list
            return render(request,self.template, {'week_slug':week_slug,'active_user':active_user, 'team_weekly_record_list':team_weekly_record_list,'week':week})
        return redirect('interface:index')

class LeagueWeekView(View):
    template = 'interface/leagueweek.html'

    def get(self, request, week_slug, league_slug):
        if not request.user.is_anonymous():
            week = int(week_slug.strip('week-'))
            active_user_id = request.user.id
            active_user = User.objects.filter(id=active_user_id)[0]
            current_league = League.objects.filter(slug=league_slug)[0]
            r = requests.get(os.environ.get('fballAPI') + week_slug + '/winners/')
            league_teams = Team.objects.filter(league=current_league)
            print(current_league)
            winners_list = r.json().get('winning_teams')
            game_count = len(winners_list)
            team_weekly_record_list = []
            for team in league_teams:
                # picks_by_team_by_week = TeamPick.objects.filter(nfl_week=week, team=team, correct=True)
                team_win_count = len(TeamPick.objects.filter(team=team, nfl_week=week, correct=True))
                team_weekly_record_list.append((team, str(team_win_count) + ' - ' + str(game_count - team_win_count)))
                # team_weekly_record_list = team_weekly_record_list
            return render(request,self.template, {'week_slug':week_slug,'active_user':active_user, 'team_weekly_record_list':team_weekly_record_list,'week':week, 'current_league':current_league})
        return redirect('interface:index')
