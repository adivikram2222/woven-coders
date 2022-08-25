from http.client import HTTPResponse
from django.http import HttpRequest
from django.shortcuts import render
from woven_app.models import Contact, Signup, Addeducationdetails

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
        # cpassword = request.POST.get('cpassword')
        address = request.POST.get('address')
        signup = Signup(email=email, fullname=fullname, aadhaar=aadhaar, phoneno=phoneno, password=password, address=address )
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
def addeducationdetails(request):
    if request.method == "POST":
        schoolname = request.POST.get('schoolname')
        previousacademic = request.POST.get('previousacademic')
        profession = request.POST.get('profession')
        standard = request.POST.get('standard')
        board_university = request.POST.get('board_university')
        addeducationdetails = Addeducationdetails(schoolname=schoolname, previousacademic=previousacademic, profession=profession,standard=standard, board_university=board_university)
        addeducationdetails.save()
    return render(request, 'eduform.html')







