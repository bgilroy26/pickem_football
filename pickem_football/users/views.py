from users.models import User,UserProfile,UserMethods
from game.models import League, Team, TeamPick
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.http import JsonResponse,Http404
import json
import requests

class GameView(View):
    def get(self,request):

        if request.session.get('_auth_user_id'):
            active_user_id =  request.session.get('_auth_user_id')
            active_user = UserMethods.objects.filter(id=active_user_id)[0]
            active_user_dict = active_user.to_json()
            # active_user_teams = Team.objects.filter(manager=active_user)
            # active_user_teams_list = [team.to_json() for team in user_teams]
            all_users = UserMethods.objects.all()
            all_users_dict = [user.to_json() for user in all_users]
            return JsonResponse({'active_user_dict':active_user_dict, 'all_users_dict': all_users_dict})
        return JsonResponse({'active_user_dict': None})

class LoginView(View):

    # def get(self,request):
    #     if request.session.get('_auth_user_id'):
    #         active_user_id = request.session.get('_auth_user_id')
    #         active_user = UserMethods.objects.filter(id=active_user_id)[0]
    #         active_user_dict = active_user.to_json()
    #         return JsonResponse({'active_user_dict':active_user_dict})
    #     return JsonResponse({'active_user_dict':None})

    def post(self,request):
        username = request.POST['username']
        password = request.POST['password']
        authenticated_user = authenticate(username=username, password=password)
        if authenticated_user:
            login(request,authenticated_user)
            auth_user = UserMethods.objects.filter(username=authenticated_user)[0]
            active_user = auth_user.to_json()
            return JsonResponse({'Success':True,'active_user':active_user})
        return JsonResponse({'Success':False})

class RegisterView(View):

    def get(self,request):
        if request.session.get('_auth_user_id'):
            active_user_id = int(request.session.get('_auth_user_id'))
            active_user_dict = UserMethods.objects.filter(id=active_user_id)[0].to_json()
            return JsonResponse({'active_user_dict':active_user_dict})
        return JsonResponse({'active_user':None})

    def post(self,request):
        submitted_username = request.POST['username']
        submitted_password = request.POST['password']
        new_user = User.objects.create_user(username = submitted_username, password = submitted_password)
        if new_user:
            new_user_profile = UserProfile(user=new_user)
            new_user_profile.save()
            authenticated_user = authenticate(username=submitted_username,password=submitted_password)
            login(request,authenticated_user)
            active_user_dict = UserMethods.objects.filter(id = int(authenticated_user.id))[0].to_json()
            return JsonResponse({'Success':True})
        return JsonResponse({'Success':False})

class LogoutView(View):

    def get(self,request):
        if request.session.get('_auth_user_id'):
            active_user_id = int(request.session.get('_auth_user_id'))
            active_user_dict = User.objects.filter(id=active_user_id)[0].to_json()
            return JsonResponse({'active_user':active_user})
        return JsonResponse({'active_user':None})

    def post(self,request):
        logout(request)
        if request.session.get('_auth_user_id'):
            return JsonResponse({'Success':False})
        return JsonResponse({'Success':True})
#
# class ProfileView(View):
#
#     def get(self,request,username):
#         if request.session.get('_auth_user_id'):
#             active_user_id = int(request.session.get('_auth_user_id'))
#             active_user_dict = UserMethods.objects.filter(id = int(active_user_id))[0].to_json()
#             if UserMethods.objects.filter(username=username):
#                 profiled_user = UserMethods.objects.filter(username=username)[0]
#                 profiled_user_dict = UserMethods.objects.filter(username=username)[0].to_json()
#                 viewed_user_profile = UserProfile.objects.filter(user=profiled_user)[0]
#                 viewed_user_profile.picture = viewed_user_profile.picture.name.strip('users/static/users/')
#                 viewed_user_profile.save()
#                 viewed_user_profile_dict = UserProfile.objects.filter(user=profiled_user)[0].to_json()
#                 viewed_user_profile.to_json()
#                 return JsonResponse({'active_user':active_user_dict,'profiled_user_dict':profiled_user_dict,'viewed_user_profile_dict':viewed_user_profile_dict})
#             return JsonResponse({'active_user':active_user_dict,'profiled_user_dict':None,'viewed_user_profile_dict':None})
#         return JsonResponse({'active_user':None})
#
#     def post(self, request, username):
#         if request.session.get('_auth_user_id'):
#             active_user_id = int(request.session.get('_auth_user_id'))
#             active_user = User.objects.filter(id=active_user_id)[0]
#             active_user_dict = UserMethods.objects.filter(id = active_user_id)[0].to_json()
#             if UserMethods.objects.filter(username=username):
#                 profiled_user = User.objects.filter(username=username)[0]
#                 viewed_user_profile = UserProfile.objects.filter(user=active_user)[0]
#                 profiled_user_dict = UserMethods.objects.filter(username=username)[0].to_json()
#                 viewed_user_profile_dict = UserProfile.objects.filter(user=active_user)[0].to_json()
#                 if active_user_id == profiled_user.id:
#                     for key, value in request.POST.items():
#                         if key == 'first_name' or key == 'last_name' or key =='email':
#
#                             setattr(profiled_user, key, value)
#                             profiled_user_dict[key]=value
#
#                             setattr(active_user, key, value)
#                             active_user_dict[key]=value
#
#                         elif key == 'about' or key == 'picture':
#                             setattr(viewed_user_profile, key, value)
#                             viewed_user_profile_dict[key]=value
#
#                     profiled_user.save()
#                     viewed_user_profile.save()
#                 return JsonResponse({'Success':True, 'active_user':active_user_dict, 'profiled_user_dict':profiled_user_dict, 'viewed_user_profile_dict':viewed_user_profile_dict})
#             return JsonResponse({'Success':False, 'active_user':active_user_dict, 'profiled_user_dict':profiled_user_dict, 'viewed_user_profile_dict':viewed_user_profile_dict})
#         return JsonResponse({'active_user':None})
#

class UserProfileView(View):

    def get(self, request, username):
        if request.session.get('_auth_user_id'):
            active_user_id = request.session.get('_auth_user_id')
            active_use_dict = UserMethods.objects.filter(id=user_id)[0].to_json()

            viewed_user = UserMethods.objects.filter(username=username)[0]
            viewed_user_dict = viewed_user.to_json()
            viewed_user_teams = Team.objects.filter(manager=viewed_user)
            viewed_user_teams_list = [team.to_json() for team in user_teams]

            return JsonResponse({'active_user_dict':active_user_dict,'viewed_user_dict':viewed_user_dict,'viewed_user_teams_list':viewed_user_teams_list})
        return JsonResponse({'active_user':None})

        #         if request.session.get('_auth_user_id'):
        #             active_user_id = int(request.session.get('_auth_user_id'))
        #             active_user_dict = UserMethods.objects.filter(id = int(active_user_id))[0].to_json()
        #             if UserMethods.objects.filter(username=username):
        #                 profiled_user = UserMethods.objects.filter(username=username)[0]
        #                 profiled_user_dict = UserMethods.objects.filter(username=username)[0].to_json()
        #                 viewed_user_profile = UserProfile.objects.filter(user=profiled_user)[0]
        #                 viewed_user_profile.picture = viewed_user_profile.picture.name.strip('users/static/users/')
        #                 viewed_user_profile.save()
        #                 viewed_user_profile_dict = UserProfile.objects.filter(user=profiled_user)[0].to_json()
        #                 viewed_user_profile.to_json()
        #                 return JsonResponse({'active_user':active_user_dict,'profiled_user_dict':profiled_user_dict,'viewed_user_profile_dict':viewed_user_profile_dict})
        #             return JsonResponse({'active_user':active_user_dict,'profiled_user_dict':None,'viewed_user_profile_dict':None})
        #         return JsonResponse({'active_user':None})
