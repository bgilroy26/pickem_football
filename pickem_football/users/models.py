from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# import re


class UserProfile(models.Model):

    about = models.TextField(max_length=700, default='[user description]')
    picture = models.ImageField(blank=True,upload_to= 'users/static/users')
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User)

    def to_json(self):

        return {'user':self.user,'created_at': self.created_at, 'updated_at':self.updated_at, 'id':self.id,'firstname':self.firstname, 'lastname':self.lastname,'picture':self.picture}
