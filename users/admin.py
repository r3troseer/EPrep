from django.contrib import admin
from .models import User, PhoneNumber

# Register your models here.
admin.site.register(User)
admin.site.register(PhoneNumber)