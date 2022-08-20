from django.contrib import admin
from django.urls import path, include
from woven_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login, name="login"),
    path('contact/',views.contact,name="contact"),
    
    
]