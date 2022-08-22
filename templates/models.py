from django.db import models
from datetime import date, datetime
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Teachers(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()
    username= models.TextField()
    gender= models.TextField()
    email = models.TextField()
    contactno = models.TextField()
    password = models.TextField()
    zipcode = models.TextField()
    subject = ArrayField(ArrayField(models.CharField(max_length=30)))
    entity_type = models.TextField(default = "teacher")

    def fetch_teacher_by_email(insertedemail):
        all_teacher = Teachers.objects.all()
        for i in all_teacher:
            if i.email == insertedemail:
                return i
        

class Students(models.Model):
    firstname = models.TextField()
    lastname = models.TextField()
    username= models.TextField()
    gender= models.TextField()
    email = models.TextField()
    contactno = models.TextField()
    password = models.TextField()
    zipcode = models.TextField()
    subject = ArrayField(ArrayField(models.CharField(max_length=30)))
    entity_type = models.TextField(default = "student")

    def fetch_teacher_by_email(insertedemail):
        all_teacher = Students.objects.all()
        for i in all_teacher:
            if i.email == insertedemail:
                return i

class Students_Teachers_Mapping(models.Model):
    teacher_username = models.TextField()
    student_username = models.TextField()
    subject = models.TextField()

class Connection_Counts_Username(models.Model):
    username = models.TextField()
    counts = models.IntegerField()


class Subscription_entries(models.Model):
    username = models.TextField()
    subscription_type = models.TextField()
    subscription_start_date = models.DateTimeField(default = date.today())

class Courses(models.Model):
    course_name = models.CharField(max_length=100)
    course_image = models.ImageField(upload_to='pics')
    course_desc = models.TextField()
    course_count = models.TextField()
    course_sub = models.TextField(default = "new")
    course_sub = models.TextField(default = "")

class Room(models.Model):
    name = models.CharField(max_length= 10000)

class Message(models.Model):
    value = models.CharField(max_length = 10000000)
    date = models.DateTimeField(default = datetime.now, blank = True)
    username = models.CharField(max_length= 1000000)
    room = models.CharField(max_length = 1000000)


# Adarsh
class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    phone = models.IntegerField()
    message = models.TextField()
    date = models.DateTimeField(default = datetime.now, blank = True)

class PaymentRecords(models.Model):
    username = models.CharField(max_length=100)
    payment_id = models.CharField(max_length=200)
    order_id = models.CharField(max_length=200)

