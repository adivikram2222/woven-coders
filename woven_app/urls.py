from django.contrib import admin
from django.urls import path, include
from woven_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('apply/', views.signup, name="login"),
    path('contact/',views.contact,name="contact"),
    
    
    
]