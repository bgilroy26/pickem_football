# from django import template
# register = template.Library()
# from game.models import League, WeeklyPicks, Game, Membership
#
# @register.inclusion_tag('game/_leagues.html')
# def active_user_leagues():
# 	all_user_leagues = League.objects.filter(user_id = user__id).order_by('-created_at')
# 	return {'all_posts': all_posts}
#
# @register.inclusion_tag('game/_picks.html')
# def user_weekly_pics():
# 	user_weekly_pics_in_league = WeeklyPicks.objects.filter(league_id=league__id, user_id=user___id).order_by('-created_at')
# 	return {'all_posts': all_posts}
#
# @register.inclusion_tag('game/_games.html')
# def get_games():
# 	all_games_by_week = League.objects.filter(user_id = user__id).order_by('-created_at')
# 	return {'all_posts': all_posts}
