from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# import re
class UserMethods(User):

      def to_json(self):
          return {'username':self.username,'date_joined': self.date_joined,'id':self.id,'first_name':self.first_name, 'last_name':self.last_name,'password':self.password,'email':self.email}

      class Meta:
          proxy=True



class UserProfile(models.Model):

    about = models.TextField(max_length=700, default='[user description]')
    picture = models.ImageField(blank=True, upload_to= 'users/static/users')
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User)

    def to_json(self):
        return {'user':self.user.username,'updated_at':self.updated_at, 'id':self.id,'picture':self.picture.name,'about':self.about}
