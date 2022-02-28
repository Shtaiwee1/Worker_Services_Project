from django.urls import path
from . import views
#urls and routes that determines the progression and redirection of pages
#it is also responsible for linking urls to functions in the views.py page to determine each pages functionality
urlpatterns = [
    path('main',views.main ,name='main'),
    path('add_field',views.add_field),
    path('profile',views.profile),
    path('edit_profile',views.edit_profile),
    path('my_workers',views.my_workers),
    path('new_worker',views.new_worker),
    path('workers_list/<int:service_id>',views.workers_group),
    path('save_contact/<int:worker_id>/<int:service_id>',views.save_contact),
    path('remove_contact/<int:worker_id>',views.remove_contact),
    
    ]
