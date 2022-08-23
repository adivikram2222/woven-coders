from django.contrib import admin
from django.urls import path, include
from woven_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('apply/', views.apply, name="login"),
    path('contact/',views.contact,name="contact"),
    path('add_education_details/',views.add_education_details,name="add_education_details"),
    
    
]