from http.client import HTTPResponse
from django.http import HttpRequest
from django.shortcuts import render
from woven_app.models import Contact

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
def login(request):
    return render(request, 'login_signup.html')
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phoneno= request.POST.get('phoneno')
        message = request.POST.get('message')
        contact = Contact(name=name, email=email, phoneno=phoneno, message=message)
        contact.save()
    return HTTPResponse('your message has been submitted successfully')