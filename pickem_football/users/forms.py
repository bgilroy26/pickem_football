from django.forms import ModelForm
from users.models import UserProfile,User
from django import forms


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }

class UserProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']

class UserExtendedProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['about', 'picture']
