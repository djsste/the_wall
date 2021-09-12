from django.db import models
import bcrypt, re
from datetime import *
from dateutil.relativedelta import *

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        all_users = User.objects.all()
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be atleast 2 characters long"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be atleast 2 characters long"
        UserRegex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-z0-9._-]+\.[a-zA-z]+$')
        print('test')
        if not UserRegex.match(postData['email']):
            errors['email'] = "This is not a valid email"
        for user in all_users:
            if user.email == postData['email']:
                errors['unique_email'] = "This email is already taken"
        user_birthday = datetime.strptime(postData['birthday'], '%Y-%m-%d')
        if user_birthday > datetime.today():
            errors["birthday_valid"] = "User birthday must be in the past!"
        if user_birthday > datetime.today() - relativedelta(years=13):
            errors["birthday_age"] = "User must be at least 13"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters long"
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Password and Confirm PW must match"
        return errors
    def login_validator(self, postData):
        errors = {}
        login_user = User.objects.filter(email=postData['logemail'])
        if len(login_user) > 0:
            if bcrypt.checkpw(postData['logpassword'].encode(), login_user[0].password.encode()):
                print('password matches')
            else:
                errors['logpassword'] = "That username and or password is incorrect"
        else:
            errors['logusername'] = "There is no account associated with that email"

        return errors
        
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.TextField(max_length=255)
    birthday = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
