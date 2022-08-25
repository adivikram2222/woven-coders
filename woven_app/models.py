from django.db import models


# Create your models here.
class Contact(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phoneno = models.CharField(max_length=12 , blank=True, null=True )
    message = models.TextField(blank=True, null=True)
    
class Signup(models.Model):
    email = models.CharField(max_length=12 , blank=True, null=True )
    fullname = models.CharField(max_length=122)
    aadhaar = models.CharField(max_length=12)
    phoneno = models.CharField(max_length = 12)
    password = models.CharField(max_length= 20)
    # cpassword = models.CharField(max_length=12, blank=True, null=True)
    address = models.CharField(max_length=200)

class Addeducationdetails(models.Model):
    schoolname = models.CharField(max_length=50)
    previousacademic = models.CharField(max_length=122)
    profession = models.TextField(null=True)
    standard = models.TextField(null=True)
    board_university = models.TextField(null=True)

class Parentaldetails(models.Model):
    fathername = models.CharField(max_length=20)
    fatheroccupation = models.CharField(max_length=30)
    fatherphonenumber = models.CharField(max_length=12)
    mothername = models.CharField(max_length=20)
    motheroccupation = models.CharField(max_length=30)
    motherphonenumber = models.CharField(max_length=12)
    address = models.CharField(max_length=50)




    
























