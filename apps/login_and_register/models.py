from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'[a-zA-Z]{2}')
PASSWORD_REGEX = re.compile(r'[a-zA-Z0-9 !\"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~"]{8}')
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def validateRegistration(self, postData):

        feedback = {
            'first_name': postData['first_name'],
            'last_name': postData['last_name'],
            'email': postData['email'],
            'username':postData['username']
        }

        result = {
             'status': False
        }

        errors = []

        if len(postData['first_name']) < 1:
            errors.append('Please enter your first name (2 or more letters only).')
            feedback["first_name"] = ""
        elif len(postData['first_name']) < 2:
            errors.append('First name must have least 2 characters.')
            feedback["first_name"] = ""
        elif not NAME_REGEX.match(postData['first_name']):
            errors.append('First name must be letters only.')
            feedback["first_name"] = ""
        if len(postData['last_name']) < 1:
            errors.append('Please enter your last name (2 or more letters only).')
            feedback["last_name"] = ""
        elif len(postData['last_name']) < 2:
            errors.append('Last name must have least 2 characters.')
            feedback["last_name"] = ""
        elif not NAME_REGEX.match(postData['last_name']):
            errors.append('Last name must be letters only.')
            feedback["last_name"] = ""
        if len(postData['username']) < 1: 
            errors.append('Please enter a username.')
        elif len(postData['username']) < 5:
            errors.append('Username must be at least 5 characters long.')
        if len(postData['email']) < 1:
            errors.append('Please enter an email.')
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append('Invalid Email.')
        if User.objects.filter(email=postData['email']).count() > 0:
            errors.append('Account '+postData['email']+' is already registered.')
            feedback["email"] = ""
        if len(postData['password']) < 1:
            errors.append('Please enter a password (8 or more characters).')
        elif len(postData['cpassword']) < 1:
            errors.append('Please confirm your password.')
        elif not PASSWORD_REGEX.match(postData['password']):
            errors.append('Password must have 8 or more characters.')
        if postData['password'] != postData['cpassword']:
            errors.append('Passwords do not match.')

        if len(errors):
            result['errors'] = errors

        else:
            result['status'] = True
            pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name = postData['first_name'],last_name = postData['last_name'], username = postData['username'], email = postData['email'],pw_hash = pw_hash)
            result['user_id'] = user.id

        result['feedback'] = feedback        

        print result
        return result


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    pw_hash = models.CharField(max_length=255)
    objects = UserManager()
    def __str__(self):
        return self.first_name,self.last_name
