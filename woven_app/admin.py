from django.contrib import admin
from woven_app.models import Contact
from woven_app.views import Signup
from woven_app.views import add_education_details


# Register your models here.
admin.site.register(Contact)
admin.site.register(Signup)
admin.site.register(add_education_details)
