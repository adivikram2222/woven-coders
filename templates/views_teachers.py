import email
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Teachers, Students, Students_Teachers_Mapping, Connection_Counts_Username,Subscription_entries, Courses, Room, Message
import random
import smtplib
import os
from twilio.rest import Client
from datetime import date 
import razorpay

# Create your views here.
def courses(request):
    courses = Courses.objects.all()
    context = {
        "courses" : courses.values()
    }
    return render(request, 'course.html', context)


def oldpage(request):
    return render(request,'index_old.html') 


def about(request):
    return render(request,'aboutus.html')       




def add_teacher_entry(request: HttpResponse):
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    email = request.POST['email']
    contactno = request.POST['contactno']
    password = request.POST['password']
    zipcode = request.POST['zipcode']
    username = request.POST['username']
    subject = request.POST['subject']
    subject = subject.split(',')
    gender = request.POST['gender']

    contactno = "+91" + str(contactno)

    # Handling Duplicate Registerations
    all_fetched_teachers = Teachers.objects.all()
    all_usernames=[]
    all_emails =[]
    for teacher in all_fetched_teachers:
        all_usernames.append(teacher.username)
        all_emails.append(teacher.email)

    if username not in all_usernames and email not in all_emails:

        #setting entires inside session before phone and email verification
        request.session['firstname'] = firstname
        request.session['lastname'] = lastname
        request.session['email'] = email
        request.session['contactno'] = contactno
        request.session['password'] = password
        request.session['zipcode'] = zipcode
        request.session['username'] = username
        request.session['subject'] = subject
        request.session['gender'] = gender

        generate_OTPs(request, email)

        return render(request, 'verifications.html')

    else:
        context = {
            "msg" : "Account already exist"
        }
        return render(request, 'login.html', context)


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



def fetching_available_teacher_as_per_location(request: HttpResponse):
    if request.session.get('entity_type') != 'teacher':
        learning_mode = request.POST['learningMode']
        zipcode = request.POST['zipCode']

        subject = request.POST['subject']
        username = request.session.get('username')

        if learning_mode == "Online":
            all_teachers = Teachers.objects.all()
            list_of_available_teachers = []
            for teacher in all_teachers:
                if subject in teacher.subject:
                    list_of_available_teachers.append(teacher)

        else:
            all_teachers = Teachers.objects.all()
            list_of_available_teachers = []
            for teacher in all_teachers:
                if subject in teacher.subject and teacher.zipcode == zipcode:
                    list_of_available_teachers.append(teacher)

        if username:
            context = {
                'teachers_list': list_of_available_teachers,
                'username': request.session.get('username'),
                'entity_type': request.session.get('entity_type')
            }
            return render(request, 'home.html', context)

        else:
            context = {
                'teachers_list': list_of_available_teachers,
            }
            return render(request, 'index.html', context)

    else:
        learning_mode = request.POST['learningMode']
        zipcode = request.POST['zipCode']

        subject = request.POST['subject']
        username = request.session.get('username')

        if learning_mode == "Online":
            all_students = Students.objects.all()
            list_of_available_students = []
            for student in all_students:
                if subject in student.subject:
                    list_of_available_students.append(student)

        else:
            all_students = Students.objects.all()
            list_of_available_students = []
            for student in all_students:
                if subject in student.subject and student.zipcode == zipcode:
                    list_of_available_students.append(student)

        if username:
            context = {
                'teachers_list': list_of_available_students,
                'username': request.session.get('username'),
                'entity_type': request.session.get('entity_type')
            }
            return render(request, 'home.html', context)

        else:
            context = {
                'teachers_list': list_of_available_students,
            }
            return render(request, 'index.html', context)



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



def student_teacher_connection(request: HttpResponse):
    username = request.session.get('username')
    if not username:
        context = {
            "msg": "Operation Cancelled, Please Login First"
        }
        return render(request, 'login.html', context)
    if request.session.get('entity_type') != 'teacher':
        teachers_email = request.POST['teachersEmail']
        student_username = request.session.get('username')
        teacher = Teachers.fetch_teacher_by_email(teachers_email)
        all_mapped_entires = Students_Teachers_Mapping.objects.filter(student_username = student_username).filter(teacher_username = teacher.username)
        if all_mapped_entires:
            return render(request, 'alreadyConnected.html')
        subscription = Subscription_entries.objects.filter(username = student_username)
        if not subscription:
            return render(request, 'sprice.html', context={
                'razorpay_key_id': os.environ.get('RAZORPAY_KEY_ID')
            })
        else:
            student_subscription_count = Connection_Counts_Username.objects.filter(username = student_username)
            if len(student_subscription_count) == 0:
                entry_for_db = Students_Teachers_Mapping(random.randint(1,10000000000), teacher.username, student_username, teacher.subject)
                entry_for_db.save()
                connections_counts_as_per_username(request, teacher.username)
                connections_counts_as_per_username(request, student_username)
                context = {
                    "username" : request.session.get('username') 
                }
                return render(request, 'home.html' ,context)

            student_subscription_count = int(student_subscription_count.counts)
            students_current_plan = subscription.subscription_type

            # Handling subscriptions count constraints as per students Plan, This will check during student teachers connection
            # When connection request will made from student side
            if students_current_plan == 'basic':
                if student_subscription_count <10:
                    entry_for_db = Students_Teachers_Mapping(random.randint(1,10000000000), teacher.username, student_username, teacher.subject)
                    entry_for_db.save()
                    connections_counts_as_per_username(request, teacher.username)
                    connections_counts_as_per_username(request, student_username)
                    context = {
                        "username" : request.session.get('username') 
                    }
                    return render(request, 'home.html' ,context)
                else:
                    return render(request, 'sprice.html', context={
                        'razorpay_key_id': os.environ.get('RAZORPAY_KEY_ID')
                    })

            elif students_current_plan == 'standerd':
                if student_subscription_count <35:
                    entry_for_db = Students_Teachers_Mapping(random.randint(1,10000000000), teacher.username, student_username, teacher.subject)
                    entry_for_db.save()
                    connections_counts_as_per_username(request, teacher.username)
                    connections_counts_as_per_username(request, student_username)
                    context = {
                        "username" : request.session.get('username') 
                    }
                    return render(request, 'home.html' ,context)
                else:
                    return render(request, 'sprice.html', context={
                        'razorpay_key_id': os.environ.get('RAZORPAY_KEY_ID')
                    })
            else:
                entry_for_db = Students_Teachers_Mapping(random.randint(1,10000000000), teacher.username, student_username, teacher.subject)
                entry_for_db.save()
                connections_counts_as_per_username(request, teacher.username)
                connections_counts_as_per_username(request, student_username)
                context = {
                    "username" : request.session.get('username') 
                }
                return render(request, 'home.html' ,context)

    # Handling Teacher Subscription
    else:
        student_email = request.POST['teachersEmail']
        teacher_username = request.session.get('username')
        student = Students.fetch_teacher_by_email(student_email)
        all_mapped_entires = Students_Teachers_Mapping.objects.filter(teacher_username = teacher_username).filter(student_username = student.username)
        if all_mapped_entires:
            return render(request, 'alreadyConnected.html')
        subscription = Subscription_entries.objects.filter(username = teacher_username)
        if not subscription:
            return render(request, 'tprice.html', context={
                'razorpay_key_id': os.environ.get('RAZORPAY_KEY_ID')
            })
        else:
            teacher_subscription_count = Connection_Counts_Username.objects.filter(username = teacher_username)
            if len(teacher_subscription_count) == 0:
                entry_for_db = Students_Teachers_Mapping(random.randint(1,10000000000), teacher_username, student.username, student.subject)
                entry_for_db.save()
                connections_counts_as_per_username(request, teacher_username)
                connections_counts_as_per_username(request, student.username)
                context = {
                    "username" : request.session.get('username') 
                }
                return render(request, 'home.html' ,context)

            teacher_subscription_count = int(teacher_subscription_count.counts)
            teacher_current_plan = subscription.subscription_type

            # Handling subscriptions count constraints as per students Plan, This will check during student teachers connection
            # When connection request will made from student side
            if teacher_current_plan == 'basic':
                if teacher_subscription_count <10:
                    entry_for_db = Students_Teachers_Mapping(random.randint(1,10000000000), teacher_username, student.username, teacher.subject)
                    entry_for_db.save()
                    connections_counts_as_per_username(request, teacher_username)
                    connections_counts_as_per_username(request, student.username)
                    context = {
                        "username" : request.session.get('username') 
                    }
                    return render(request, 'home.html' ,context)
                else:
                    return render(request, 'tprice.html', context={
                        'razorpay_key_id': os.environ.get('RAZORPAY_KEY_ID')
                    })

            elif teacher_current_plan == 'standerd':
                if teacher_subscription_count <35:
                    entry_for_db = Students_Teachers_Mapping(random.randint(1,10000000000), teacher_username, student.username, teacher.subject)
                    entry_for_db.save()
                    connections_counts_as_per_username(request, teacher_username)
                    connections_counts_as_per_username(request, student.username)
                    context = {
                        "username" : request.session.get('username') 
                    }
                    return render(request, 'home.html' ,context)
                else:
                    return render(request, 'tprice.html', context={
                        'razorpay_key_id': os.environ.get('RAZORPAY_KEY_ID')
                    })
            else:
                entry_for_db = Students_Teachers_Mapping(random.randint(1,10000000000), teacher_username, student.username, teacher.subject)
                entry_for_db.save()
                connections_counts_as_per_username(request, teacher_username)
                connections_counts_as_per_username(request, student.username)
                context = {
                    "username" : request.session.get('username') 
                }
                return render(request, 'home.html' ,context)

def connections_counts_as_per_username(request, passed_username):
    all_enteries = Connection_Counts_Username.objects.all()
    flag = False
    for i in all_enteries:
        if i.username == passed_username:
            i.counts = i.counts+1
            i.save()
            flag = True
            break;

    if not flag:
        fetched_entry = Connection_Counts_Username(random.randint(1,10000000000), passed_username, 1)
        fetched_entry.save()


def subscription_request(request):
    if request.session.get('entity_type') != "teacher":
        price_map = {
            "basic": 9900,
            "standerd":28000,
            "premium":55000
        }
    else:
        price_map = {
            "basic": 19900,
            "standerd":56000,
            "premium":110000
        }

    try:
        if request.method == "POST":
            username = request.session.get('username')
            subscription_type = request.POST['subscription_type']
            amount = price_map[subscription_type]
            
            client = razorpay.Client(
                auth=(os.environ.get('RAZORPAY_KEY_ID'), os.environ.get('RAZORPAY_KEY_SECRET')))

            payment = client.order.create({'amount': amount, 'currency': 'INR',
                                        'payment_capture': '1'})
            today = date.today()
            entry = Subscription_entries(random.randint(1,10000000000000), username, subscription_type, today)
            entry.save()
            context = {
                "username" : request.session.get('username') 
            }
            return render(request, 'home.html' ,context)

    except:
        return render(request, 'sprice.html', context={
            'razorpay_key_id': os.environ.get('RAZORPAY_KEY_ID')
        })


def studentHomePage(request):
    username = request.session.get('username')

    # Fetching current user's details like name , email etc.
    student_details = {}
    temp_rec = Students.objects.filter(username = username)
    temp = temp_rec.values()[0]
    student_details['username'] = temp['username']
    student_details['name'] = temp['firstname']+ ' ' + temp['lastname']
    student_details['email'] = temp['email']
    student_details['zipcode'] = temp['zipcode']
    student_details['subject'] = temp['subject']
    student_details['contact'] = temp['contactno']

    temp_rec = Subscription_entries.objects.filter(username = username)
    if len(temp_rec) == 0:
        student_details['subscription'] = 'N/A'
    else:
        temp = temp_rec.values()[0]
        student_details['subscription'] = temp['subscription_type']


    # Fetching connected Teachers details
    temp_rec = Students_Teachers_Mapping.objects.filter(student_username = username)
    temp_rec = temp_rec.values()
    connected_teachers_list = []
    for rec in temp_rec:
        connected_teachers_list.append(rec['teacher_username'])

    teachers_details = []
    for rec in connected_teachers_list:
        fetch_current_teacher = Teachers.objects.filter(username = rec)
        fetch_current_teacher = fetch_current_teacher.values()[0]
        temp = {}
        temp['teacher_name'] = fetch_current_teacher['firstname'] +' '+ fetch_current_teacher['lastname']
        temp['teacher_contact_number'] = fetch_current_teacher['contactno']
        temp['teacher_email'] = fetch_current_teacher['email']
        temp['sub'] = fetch_current_teacher['subject']
        temp['teacher_username'] = fetch_current_teacher['username']
        teachers_details.append(temp)

    student_details['connected_teachers'] = teachers_details
    context = student_details
    return render(request, 'studentHomePage.html', context )

def teacherHomePage(request):
    username = request.session.get('username')

    # Fetching current user's details like name , email etc.
    teacher_details = {}
    temp_rec = Teachers.objects.filter(username = username)
    temp = temp_rec.values()[0]
    teacher_details['username'] = temp['username']
    teacher_details['name'] = temp['firstname']+ ' ' + temp['lastname']
    teacher_details['email'] = temp['email']
    teacher_details['zipcode'] = temp['zipcode']
    teacher_details['subject'] = temp['subject']
    teacher_details['contact'] = temp['contactno']

    temp_rec = Subscription_entries.objects.filter(username = username)
    if len(temp_rec) == 0:
        teacher_details['subscription'] = 'N/A'
    else:
        temp = temp_rec.values()[0]
        teacher_details['subscription'] = temp['subscription_type']


    # Fetching connected Teachers details
    temp_rec = Students_Teachers_Mapping.objects.filter(teacher_username = username)
    temp_rec = temp_rec.values()
    connected_students_list = []
    for rec in temp_rec:
        connected_students_list.append(rec['student_username'])

    student_details = []
    for rec in connected_students_list:
        fetch_current_student = Students.objects.filter(username = rec)
        fetch_current_student = fetch_current_student.values()[0]
        temp = {}
        temp['student_name'] = fetch_current_student['firstname'] +' '+ fetch_current_student['lastname']
        temp['student_contact_number'] = fetch_current_student['contactno']
        temp['student_email'] = fetch_current_student['email']
        temp['student_username'] = fetch_current_student['username']
        student_details.append(temp)

    teacher_details['connected_students'] = student_details
    context = teacher_details
    return render(request, 'teacherHomePage.html', context )

def index(request):
    username = request.session.get('username')
    if username:
        # Clearing Session On Logout
        del request.session['username']
        courses = Courses.objects.all()
        context = {
            "courses" : courses.values()
        }
        return render(request, 'index.html', context)

    else:
        courses = Courses.objects.all()
        context = {
            "courses" : courses.values()
        }
        return render(request, 'index.html', context)

def home(request):
    username = request.session.get('username')
    entity_type = request.session.get('entity_type')
    courses = Courses.objects.all()
    context = {
        "courses" : courses.values(),
        "username": username, 
        "entity_type": entity_type
    }
    return render(request, 'home.html', context)

def chat(request, room):
    username = request.session.get('username')
    room_details = Room.objects.get(name= room)
    return render(request, 'chatbox.html', {
        'username':username,
        'room':room,
        'room_details':room_details
    })

def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']

    if Room.objects.filter(name = room).exists():
        return redirect('/' + room+'/?username'+username)
    else:
        new_room = Room.objects.create(name = room)
        new_room.save()
        return redirect('/' + room+'/?username'+username)

def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value = message, username= username, room = room_id)
    new_message.save()
    return HttpResponse('message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    return JsonResponse({"messages":list(messages.values())})




# Adarsh
def contact(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        email = request.POST['email']
        phone = request.POST['phone']
        subject = request.POST['subject']
        new_contact = Contact.objects.create(firstname = firstname, email = email, phone = phone, subject = subject)
        new_contact.save()
    return HttpResponse('message sent successfully')


def courses(request):
    courses = Courses.objects.all()
    context = {
        "courses" : courses.values()
    }
    return render(request, 'course.html', context)


def oldpage(request):
    return render(request,'index_old.html')    


# Teacher Update details
def edit_teachers_details(request):
    context = {}
    return render(request, 'edit_teacher_details.html', context)

def update_teacher_details(request):
    if request.method == 'POST':
        #formetting subjects as array
        subject = request.POST['subject']
        subject = subject.split(',')
        current_username = request.session.get('username')
        current_user_object = Teachers.objects.filter(username = current_username).update(email = request.POST['email'], \
                        contactno = request.POST['contact'], zipcode = request.POST['zip'], subject = subject)

    username = request.session.get('username')
    entity_type = request.session.get('entity_type')
    courses = Courses.objects.all()
    context = {
        "courses" : courses.values(),
        "username": username, 
        "entity_type": entity_type
    }
    return render(request, 'home.html', context)


# Students Update Details
def edit_student_details(request):
    context = {}
    return render(request, 'edit_student_details.html', context)

def update_student_details(request):
    if request.method == 'POST':
        #formetting subjects as array
        subject = request.POST['subject']
        subject = subject.split(',')
        current_username = request.session.get('username')
        current_user_object = Students.objects.filter(username = current_username).update(email = request.POST['email'], \
                        contactno = request.POST['contact'], zipcode = request.POST['zip'], subject = subject)

    username = request.session.get('username')
    entity_type = request.session.get('entity_type')
    courses = Courses.objects.all()
    context = {
        "courses" : courses.values(),
        "username": username, 
        "entity_type": entity_type
    }
    return render(request, 'home.html', context)
