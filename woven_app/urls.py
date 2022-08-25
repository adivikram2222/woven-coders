from django.contrib import admin
from django.urls import path, include
from woven_app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('apply/', views.apply, name="login"),
    path('contact/', views.contact,name="contact"),
    path('addeducationdetails/', views.addeducationdetails,name="addeducationdetails"),
    path('parentaldetails/',views.parentaldetails, name="parentaldetails")
    
    
]