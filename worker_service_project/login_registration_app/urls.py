from django.urls import path
from . import views
#urls and routes that determines the progression and redirection of pages
#it is also responsible for linking urls to functions in the views.py page to determine each pages functionality
urlpatterns = [
    path('', views.index),#root_page
    path('join_us', views.join_form),#root_page
    path('check_login', views.check),#process login form
    path('user/create', views.create_user),#After logging out the users session is cleared to prevent access to the success page without logging in
    path('destroy', views.delete),]#After logging out the users session is cleared to prevent access to the success page without logging in
