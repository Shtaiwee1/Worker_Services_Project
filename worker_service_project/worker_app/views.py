from unicodedata import name
from django.shortcuts import render , redirect
from django.contrib import messages#import error messages for display
import bcrypt#importing bcrypt after installing using pip install bcrypt used for hashing,encoding and decoding
from login_registration_app.models import User , Worker , Service#importing class from models.py

#root page


def main(request):
    this_user=User.objects.get(id=request.session['userid'])
    context={"all_services":Service.objects.all(),
            "current_user":this_user}
    return render(request,'Main.html',context)

def add_field(request):
    name=request.POST['name']
    description=request.POST['description']
    new_service=Service.objects.create(name=name,description=description)
    
    return redirect('/main')

def profile(request):
    this_user=User.objects.get(id=request.session['userid'])
    context={"all_services":Service.objects.all(),
            "current_user":this_user}
    return render(request,'edit.html',context)

def edit_profile(request):
    this_user=User.objects.get(id=request.session['userid'])
    this_user.first_name=request.POST['updated_first_name']
    this_user.last_name=request.POST['updated_last_name']
    this_user.email=request.POST['updated_email']
    this_user.save()
    return redirect('/profile')

def new_worker(request):
    this_user=User.objects.get(id=request.session['userid'])
    first_name=this_user.first_name
    last_name=this_user.last_name
    email=this_user.email
    password=this_user.password
    phone_number=request.POST['phone_number']
    location=request.POST['location']
    career=request.POST['career']
    price=request.POST['price']
    desc=request.POST['desc']
    this_service=Service.objects.get(name=request.POST['career'])
    Worker.objects.create(first_name=first_name,
                        last_name=last_name,
                        email=email,
                        password=password,
                        phone_number=phone_number,
                        location=location,
                        career=career,
                        price=price,
                        desc=desc,
                        service=this_service)
    return redirect('/join_us')

def my_workers(request):
    this_user=User.objects.get(id=request.session['userid'])
    references=this_user.workers.all()
    context={"all_services":Service.objects.all(),
            "all_workers":Worker.objects.all(),
            "current_user":this_user,
            "my_references":references}
    return render(request,'my_workers.html',context)

def workers_group(request , service_id):
    this_user=User.objects.get(id=request.session['userid'])
    the_service = Service.objects.get(id=service_id)
    this_service=User.objects.get(id=service_id)
    workers_in_service=Worker.objects.filter(service_id=service_id)
    print(the_service.name)
    context={"this_service":this_service,
            "workers_in_this_service":workers_in_service,
            "current_user":this_user,
            "the_service" :the_service
            }
    return render(request,'Workers.html',context)

def save_contact(request , worker_id,service_id):
    this_user=User.objects.get(id=request.session['userid'])
    this_worker=Worker.objects.get(id=worker_id)
    this_user.workers.add(this_worker)
    return redirect(f'/workers_list/{service_id}')

def remove_contact(request , worker_id):
    this_user=User.objects.get(id=request.session['userid'])
    this_worker=Worker.objects.get(id=worker_id)
    this_user.workers.remove(this_worker)
    return redirect('/my_workers')