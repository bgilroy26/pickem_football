from django.forms import ModelForm
from users.models import UserProfile,User


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']

class UserExtendedProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['about', 'picture']
