from http.client import HTTPResponse
from django.http import HttpRequest
from django.shortcuts import render
from woven_app.models import Contact, Signup


import email
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

import random
import smtplib
import os
from twilio.rest import Client
from datetime import date 


from .models import Students, Teachers, Courses 



# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phoneno= request.POST.get('phoneno')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phoneno=phoneno, message = message)
        contact.save()
    return render(request, 'index.html')
def apply(request):
    if request.method == "POST": 
        email = request.POST.get('email')
        fullname = request.POST.get('fullname')
        aadhaar = request.POST.get('aadhaar')
        phoneno = request.POST.get('phoneno')
        password = request.POST.get('password')
        address = request.POST.get('address')
        signup = Signup(email=email, fullname=fullname, aadhaar=aadhaar, phoneno=phoneno, password=password, address=address)
        signup.save()
    return render(request, 'signup.html')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phoneno= request.POST.get('phoneno')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phoneno=phoneno, message=message)
        contact.save()
    return HTTPResponse('your message has been submitted successfully')






def add_student_entry(request: HttpResponse):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    contactno = request.POST['contactno']
    password = request.POST['password']
    zipcode = request.POST['zipcode']
    username = request.POST['username']
    gender = request.POST['gender']
    subject = request.POST['subject']

    subject = subject.split(',')

    
    contactno = "+91" + str(contactno)

    # Handling Duplicate Registerations
    all_fetched_students = Students.objects.all()
    all_usernames = []
    all_emails = []

    for student in all_fetched_students:
        all_usernames.append(student.username)
        all_emails.append(student.email)

    if username not in all_usernames and email not in all_emails:
        
        #setting entires inside session before phone and email verification
        request.session['firstname'] = firstname
        request.session['lastname'] = lastname
        request.session['email'] = email
        request.session['contactno'] = contactno
        request.session['password'] = password
        request.session['zipcode'] = zipcode
        request.session['username'] = username
        request.session['gender'] = gender
        request.session['subject'] = subject

        generate_OTPs(request, email)

        return render(request, 'verification2.html')

    else:
        context = {
            "msg" : "Account already exist"
        }
        return render(request, 'login.html', context)



def login(request: HttpResponse):
    courses = Courses.objects.all()
    courses = courses.values()
    username = request.POST['username']
    password = request.POST['password']

    all_teachers = Teachers.objects.all()
    for i in all_teachers:
        if i.username == username and i.password == password:
            request.session['username'] = i.username
            request.session['email'] = i.email
            request.session['entity_type'] = i.entity_type
            context = {
                "username" : request.session.get('username'),
                "entity_type": request.session.get('entity_type'),
                "courses":courses
            }
            return render(request, 'index.html' ,context)

    all_students = Students.objects.all()
    for i in all_students:
        if i.username == username and i.password == password:
            request.session['username'] = i.username
            request.session['email'] = i.email
            request.session['entity_type'] = i.entity_type
            context = {
                "username" : request.session.get('username'),
                "entity_type": request.session.get('entity_type'),
                "courses":courses
            }
            return render(request, 'index.html' ,context)


    context = {
        "msg":"Invalid Username or Password"
    }
    return render(request, 'login.html', context)




def generate_OTPs(request, email_id):

    #OTP for email
    server_for_email = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server_for_email.ehlo()
    server_for_email.login(os.environ.get('EMAIL'),os.environ.get('PASSWORD'))
    temp_otp = random.randint(100000000,999999999)
    request.session['email_OTP'] = temp_otp
    server_for_email.sendmail(os.environ.get('EMAIL'),request.session.get('email'),str(temp_otp))
    print("email sent successfully")

    #OTP for phone-number
    temp_otp = random.randint(100000,999999)
    request.session['phoneOTP'] = temp_otp
    account_sid = os.environ.get('ACCOUNT_SID')
    auth_token = os.environ.get('AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body =f"Your OTP is {temp_otp}",
        from_ = os.environ.get('TWILIO_NUMBER'),
        to = request.session.get('contactno')
    )

    print(message.sid, "OTP sent successfully")
    


#This is for teacehers
def validator(request: HttpResponse):
    # teachers = Teachers(random.randint(1,10000000000),request.session.get('firstname'), request.session.get('lastname'), request.session.get('username'), request.session.get('gender'), request.session.get('email'),request.session.get('contactno'), request.session.get('password'), request.session.get('zipcode'), request.session.get('subject'))
    # teachers.save()
    # context = {
    #     "msg":"You have been registered successfully."
    # }
    # request.session = {}
    # return render(request, 'login.html', context)

    if (request.POST['email_otp'] == str(request.session.get('email_OTP'))) and (request.POST['phone_otp'] == str(request.session.get('phoneOTP'))):
        teachers = Teachers(random.randint(1,10000000000),request.session.get('firstname'), request.session.get('lastname'), request.session.get('username'), request.session.get('gender'), request.session.get('email'),request.session.get('contactno'), request.session.get('password'), request.session.get('zipcode'), request.session.get('subject'))
        teachers.save()
        context = {
            "msg":"You have been registered successfully."
        }
        request.session = {}
        return render(request, 'login.html', context)
    else:
        context = {
            "msg" : "Invalid OTP"
        }
        return render(request, 'login.html', context)

#This is for STudents
def validator2(request: HttpResponse):
    # student = Students(random.randint(1,10000000000),request.session.get('firstname'), request.session.get('lastname'), request.session.get('username'), request.session.get('gender'), request.session.get('email'),request.session.get('contactno'), request.session.get('password'), request.session.get('zipcode'),request.session.get('subject'))
    # student.save()
    # context = {
    #     "msg":"You have been registered successfully."
    # }
    # request.session = {}
    # return render(request, 'login.html', context)

    if (request.POST['email_otp'] == str(request.session.get('email_OTP'))) and (request.POST['phone_otp'] == str(request.session.get('phoneOTP'))):
        student = Students(random.randint(1,10000000000),request.session.get('firstname'), request.session.get('lastname'), request.session.get('username'), request.session.get('gender'), request.session.get('email'),request.session.get('contactno'), request.session.get('password'), request.session.get('zipcode'),request.session.get('subject'))
        student.save()
        context = {
            "msg":"You have been registered successfully."
        }
        request.session = {}
        return render(request, 'login.html', context)
    else:
        context = {
            "msg" : "Invalid OTP"
        }
        return render(request, 'login.html', context)

