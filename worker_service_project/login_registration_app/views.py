from django.http import HttpResponse
from django.shortcuts import render , redirect
from django.contrib import messages#import error messages for display
import bcrypt#importing bcrypt after installing using pip install bcrypt used for hashing,encoding and decoding
from .models import User , Worker , Service#importing class from models.py

#root page
def index(request):
    context={"all_users":User.objects.all()}
            #passes the models attributes to the rendered page
    return render(request, "log_reg.html",context)
#registration information processing function and validation

def check(request):
    errors = User.objects.basic_validator_second(request.POST)
    request.session["coming_from"]="LOGIN"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')#if there are any errors redirect to the root page no access for the success page
    else:
        user = User.objects.filter(email=request.POST['email_login'])#searches the database for the email input in the login form
        if user: #if there is a user with the input email = true
            logged_user = user[0]#save the user info ina varibale called logged_user
        #check if the password form thelogin form equals the hashed password in the database
        #converts the password from the form from string to byte and the hashed password in the database from hash to byte and compares the two of them 
        if bcrypt.checkpw(request.POST['password_login'].encode(), logged_user.password.encode()):#if the passwords match redirect to success page and save the logged in users info to display them in the success page
            request.session['userid'] = logged_user.id
            request.session['firstname'] = logged_user.first_name
            request.session['lastname'] = logged_user.last_name
            request.session['email'] = logged_user.email
            return redirect('/main')
    return redirect('/')#if passwords don't match redirect to root page to let the user try again

def delete(request):#the logout button redirects to the (destroy) route in the urls.py and then induces this function in the views.py to clear logged user info
    request.session.clear()
    return redirect('/')
    # user_log_out=User.objects.get(id=user_id)
    # user_log_out.delete()
    # log_out_user=User.objects.get(id=user_id)

def join_form(request):
    this_user=User.objects.get(id=request.session['userid'])
    context={"all_services":Service.objects.all(),
            "current_user":this_user,}
    return render(request, "join_workers.html",context)

def create_user(request):
    errors = User.objects.basic_validator(request.POST)
    request.session["coming_from"]="Register"
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    first_name=request.POST['first_name']
    last_name=request.POST['last_name']
    email=request.POST['email']
    password=request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=pw_hash)
    return redirect('/main')


