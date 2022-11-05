from django.contrib import admin
from .models import PayHistory, Plan, UserPlan, Subscription
# Register your models here.
admin.site.register(PayHistory)
admin.site.register(Plan)
admin.site.register(UserPlan)
admin.site.register(Subscription)
