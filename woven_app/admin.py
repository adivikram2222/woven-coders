from django.contrib import admin
from woven_app.models import Contact
from woven_app.views import Signup

# Register your models here.
admin.site.register(Contact)
admin.site.register(Signup)
