from django import template
register = template.Library()
from users.models import User


@register.inclusion_tag('blog/_users.html')
def list_users():
	all_users = User.objects.all().order_by('-member_since')
	return {'all_users': all_users}
