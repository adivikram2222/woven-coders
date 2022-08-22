from django.db import models

# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phoneno = models.CharField(max_length=12 , blank=True, null=True )
    message = models.TextField(blank=True, null=True)
    
class Signup(models.Model):
    email = models.CharField(max_length=122)
    fullname = models.CharField(max_length=122)
    aadhaar = models.CharField(max_length=12)
    phoneno = models.CharField(max_length = 12)
    password = models.CharField(max_length= 20)
    address = models.CharField(max_length=200)

























