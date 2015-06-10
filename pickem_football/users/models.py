from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
# import re


class UserProfile(models.Model):

    # def validate_username(submitted_username):
    #     if User.objects.filter(username=submitted_username):
    #         raise ValidationError("This name is already taken.")
    #     if not re.match(r'[a-zA-Z]+[a-z0-9A-Z]{3,20}', submitted_username):
    #         raise ValidationError("Name must start with a letter and contain only alphanumeric keys.")
    #
    # def validate_password(submitted_password):
    #     if not re.match(r'[a-zA-Z]+[a-z0-9A-Z]{7,20}', submitted_password):
    #         raise ValidationError("Password must be between 7 and 20 alphanumeric characters.")

    # username = models.CharField(max_length=20,unique=True,validators=[validate_username])
    # password = models.CharField(max_length=255,validators=[validate_password])
    # firstname = models.CharField(max_length=30, Default=None)
    # lastname = models.CharField(max_length=30, Default=None)
    about = models.TextField(default='[user description]')
    picture = models.ImageField()
    # created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(User)

    def to_json(self):

        return {'user':self.user,'created_at': self.created_at, 'updated_at':self.updated_at, 'id':self.id,'firstname':self.firstname, 'lastname':self.lastname,'picture':self.picture}
