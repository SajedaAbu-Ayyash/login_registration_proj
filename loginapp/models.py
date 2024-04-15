import re

from django.db import models
import bcrypt
from django.contrib import messages


class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First Name must be at least 2 characters."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last Name must be at least 2 characters."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Please enter a valid email e.g: example@example.com"
        if User.objects.filter(email=postData['email']).exists():
            errors['email'] = "Email address already exist."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters."
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = "Confirmation password does not match."
        return errors

    def log_validation(self, request):
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                return {}
        return {'error': 'Username or password is wrong'}


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


# this function for registration
def register(request):
    if request.method == 'POST':
        # validate data
        errors = User.objects.validator(request.POST)
        # if the errors dict contain anything, redirect to root route to fix errors
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)

        # if we dont have any problem redirect to wall page
        else:
            new_user = User.objects.create(first_name=request.POST['first_name'],
                                           last_name=request.POST['last_name'],
                                           email=request.POST['email'],
                                           password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode(),
                                           )
            request.session['user_id'] = new_user.id


# this function for login, check if the email/pass matches a valid email/pass in db
def log_in(request):
    if request.method == 'POST':
        errors = User.objects.log_validation(request)
        # if the errors dict contain anything
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            user = User.objects.get(email=request.POST['email'])
            request.session['user_id'] = user.id

    # if request.method == 'POST':
    #     user = User.objects.get(email = request.POST['email'])
    #     if bcrypt.checkpw(request.POST['password'].encode().user.pw_hash.encode()):
    #         print('Password match')
    #     else:
    #         print('failed password')

# Create your models here.
