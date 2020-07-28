from django.db import models
import bcrypt
import re


# Create your models here.
class UserManager(models.Manager):
    def registration_validation(self, postData):
        errors = {}

        # first_name 2 char min
        if len(postData['first_name'])<2: #eventually need to validate for too large of values as well
            errors['first_name'] = 'First name must be at least 2 characters'

        # last_name 2 char min
        if len(postData['last_name'])<2:
            errors['last_name'] = 'Last name must be at least 2 characters'

        # password 8 char min
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'

        # check that pass and conf pass match
        elif postData['password'] != postData['confirm_password']:
            errors['password'] = 'Password and confirmation do not match'

        # email regex check
        email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_REGEX.match(postData['email']):
            errors['email'] = "invalid email address!"
        else:
            # email unique check
            Users = User.objects.all()
            print('******no issues with db')
            for user in Users:
                if user.email == postData['email']:
                    errors['email'] = 'email in use'        

        return errors

    def login_validation(self, postData):
        if postData['email'] == '' or postData['password'] == '':
            error = 'email or password are invalid'
            return error

        #attempt to find user by email in db otherwise return error message     
        try:
            print("__________line 45____________")
            user = User.objects.filter(email=postData['email'])[0]
        except:
            print('____________line 47________')
            error = 'mail or password are invalid'
            return error

        #return true indicating user's login has been validated!
        if bcrypt.checkpw(postData['password'].encode(), user.hashed_pass.encode()):
            return True
        
        else:
            error = 'email or password are invalid'
            return error

    def hash_pass(self, password):
        hashed_pass = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        return hashed_pass
    
    def register_user(self, postData):        
        new_user = self.create(
            first_name = postData['first_name'], 
            last_name = postData['last_name'],
            email = postData['email'],
            hashed_pass = self.hash_pass(postData['password'])
        )
        new_user.save()

        return new_user.id

    def update_user(self, postData, user):
        errors = {}

        # first_name 2 char min
        if len(postData['first_name'])<2: #eventually need to validate for too large of values as well
            errors['first_name'] = 'First name must be at least 2 characters'

        # last_name 2 char min
        if len(postData['last_name'])<2:
            errors['last_name'] = 'Last name must be at least 2 characters'

         # email regex check
        email_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not email_REGEX.match(postData['email']):
            errors['email'] = "invalid email address!"
        else:
            #check that the email is not in use by someone else
            print(user.id)
            users = User.objects.all().exclude(id=user.id)
            print(users[0].id)
            for u in users:
                if u.email == postData['email']:
                    errors['email'] = 'email in use'

        # if no errors perform update!
        if len(errors)==0:
            user.first_name = postData['first_name']
            user.last_name = postData['last_name']
            user.email = postData['email']
            user.save()
        
        return errors

        



class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    hashed_pass = models.CharField(max_length=60)
    objects = UserManager()
