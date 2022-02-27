import email
from django.db import models
import re#importing regular expression to utillization
from datetime import datetime#import datetime for usage in the birthday error

#The manager class must be added before the main class
class UserManager(models.Manager):#Manager class to customize error messages and manage objects in the parent model (User)
    #fisrt validator for the registration form
    def basic_validator(self, postData):#a function that contains errors conditions and imports data posted from forms to validate them and use them in error functions
        errors = {}#an empty dictionary called errors to store errors that occur and call them on the view.py file #contains error messages
        #email regular expression to validate the right format for emails
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        #characters input length error for first_name
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        #characters input length error for last_name
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        #email validation right format error    
        if not EMAIL_REGEX.match(postData['email']):                
            errors['invalid_email'] = "Invalid email address!"
        # email uniqueness error
        #searches the database for existing emails using filter and saving it in an
        email_validate_unique=User.objects.filter(email=postData['email'])
        if len(email_validate_unique)> 0:
            errors['email'] = "email already exists!"
        #password errors
        #password length smaller than 18 characters error
        if len(postData['password']) < 18:
            errors["password"] = "Password should be at least 18 characters"
        #password confirmation error
        if postData['password'] != postData['confirm']:
            errors["confirm"] = "Passwords doesn't match"
        #birthday errors
        #birthday empty field error #birthday is required
        if len(postData['birthday']) < 1:
            errors["birthday"]="Date of Birth is required" 
        #birthday can't be in the future error
        else:
            birthdate = datetime.strptime(postData["birthday"], "%Y-%m-%d")
            if birthdate > datetime.now():
                errors["birthday_date"]="Date of Birth must be in the past"
        return errors   
    #second validater for the login form
    def basic_validator_second(self, postData):
        errors = {}
        #email validation right format error for the login form
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_login']):                
            errors['email-login'] = "Invalid email address!"
        #password length smaller than 18 characters error
        if len(postData['password_login']) < 8:
            errors["password-login"] = "Password should be at least 18 characters"
        return errors
#the User class and its attributes
class User(models.Model):
    #id is automatically added to the database in django
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects=UserManager()#objects attribute functionality extended using built in manager class


class ServiceManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData['name']) < 3:
            errors["name"] = "Service name should be at least 3 characters"
        if len(postData['description']) < 10:
            errors["description"] = "Service description should be at least 10 characters"
        return errors



class Service(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default="goodn")
    users = models.ManyToManyField(User, related_name="services")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ServiceManager()

    
    
class Worker(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    phone_number=models.IntegerField(default=0)
    price=models.IntegerField(default=0)
    location=models.CharField(max_length=255)
    career=models.CharField(max_length=255)
    desc=models.TextField(default="good")
    users = models.ManyToManyField(User, related_name="workers")
    service = models.ForeignKey(Service, related_name="workers", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)