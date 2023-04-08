from django.db import models
from api.models import SubLevel, Level
from users.models import User
from django.db.models.signals import post_save, pre_save, pre_init
from django.dispatch import receiver


import datetime
from datetime import timedelta
from datetime import datetime as dt

today = datetime.date.today()


PERIOD_DURATION = (
    ('1M', '1 Month'),
    ('3M', '3 Months'),
    ('12M', '12 Months'),
)


class PayHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    paystack_charge_id = models.CharField(
        max_length=100, default='', blank=True)
    paystack_access_code = models.CharField(
        max_length=100, default='', blank=True)
    payment_for = models.ForeignKey(
        SubLevel, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class Plan(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    sublevel = models.ForeignKey(SubLevel, on_delete=models.CASCADE, null=True)
    duration = models.PositiveIntegerField(default=7)
    duration_period = models.CharField(
        max_length=100, default='1M', choices=PERIOD_DURATION)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'{self.level.name}: {self.sublevel.name} for {self.duration_period}'

    # User Membership


class UserPlan(models.Model):
    user = models.OneToOneField(
        User, related_name='user_plan', on_delete=models.CASCADE)
    plan = models.ForeignKey(
        Plan, related_name='user_plan', on_delete=models.SET_NULL, null=True)
    reference_code = models.CharField(max_length=200, default='', blank=True)

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=UserPlan)
def create_subscription(sender, instance, *args, **kwargs):
    if instance:
        Subscription.objects.create(user_plan=instance,
                                    expires_in=dt.now().date() + timedelta(days=instance.plan.duration))


# User Subscription
class Subscription(models.Model):
    user_plan = models.ForeignKey(
        UserPlan, related_name='subscription', on_delete=models.CASCADE, default=None)
    expires_in = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user_plan.user)


# @receiver(pre_init, sender=Level)
# def update_active(sender, *args, **kwargs):
#     instance = Subscription.objects.filter(expires_in__lt=today)
#     # print('intiated sub check')
#     if instance:
#         for i in instance:
#             sub = Subscription.objects.get(id=i.id)
#             # print(f'{sub}|sub check')
#             sub.active = False
#             sub.save()
#             # print('sub check done')
#             # sub.delete()
