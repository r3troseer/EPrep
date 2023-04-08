from django.contrib import admin
from .models import User, PhoneNumber, Parent, Student

# Register your models here.
admin.site.register(User)
admin.site.register(PhoneNumber)
admin.site.register(Parent)
admin.site.register(Student)
