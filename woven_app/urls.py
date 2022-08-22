from django.contrib import admin
from django.urls import path, include
from woven_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('apply/', views.apply, name="login"),
    path('contact/',views.contact,name="contact"),
    path('add_students/', views.add_student_entry, name="add_students" ),
    
]