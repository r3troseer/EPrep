import datetime
import requests
from api.models import Level, SubLevel
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser
from rest_framework.exceptions import NotAcceptable
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.db.models.signals import post_save
from django.dispatch import receiver


class PhoneNumber(models.Model):
    # user = models.OneToOneField(
    #     User, on_delete=models.CASCADE)
    phone_no = models.CharField(max_length=14, unique=True)
    code = models.CharField(max_length=6)
    verified = models.BooleanField(default=False)
    sent = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.phone_no

    def test(self):
        pass

    def generate_code(self):
        """
        Returns a unique random `code` for given `TOKEN_LENGTH` in the settings.
        Default token length = 6
        """
        token_length = getattr(settings, "TOKEN_LENGTH", 6)
        return get_random_string(token_length, allowed_chars="0123456789")

    def is_code_expired(self):
        expiration_date = self.sent + datetime.timedelta(
            minutes=settings.TOKEN_EXPIRE_MINUTES
        )
        return expiration_date <= timezone.now()

    def send_confirmation(self):
        # termii_key = settings.TERMII_KEY
        # url = "https://termii.com/api/sms/send"
        # self.code = self.generate_code()
        # print(
        #  f'Sending security code {self.code} to phone {self.phone_no}')
        # payload = {
        #         "to": str(self.phone_no),
        #         "from": "eprep",
        #         "sms": f"Hi there, testing Termii {self.code}",
        #         "type": "plain",
        #         "channel": "generic",
        #         "api_key": termii_key,
        # }
        # headers = {
        # 'Content-Type': 'application/json',
        # }
        # self.sent = timezone.now()
        # self.save()
        # response = requests.request("POST", url, headers=headers, json=payload)
        # print(response.text)
        twilio_account_sid = settings.TWILIO_ACCOUNT_SID
        twilio_auth_token = settings.TWILIO_AUTH_TOKEN
        twilio_phone_number = settings.TWILIO_PHONE_NUMBER

        self.code = self.generate_code()

        print(
            f'Sending security code {self.code} to phone {self.phone_no}')

        if all(
            [
                twilio_account_sid,
                twilio_auth_token,
                twilio_phone_number
            ]
        ):
            try:
                twilio_client = Client(
                    twilio_account_sid, twilio_auth_token
                )
                twilio_client.messages.create(
                    body=f'Your activation code is {self.code}',
                    to=str(self.phone_no),
                    from_=twilio_phone_number,
                )
                self.sent = timezone.now()
                self.save()
                print(f'{self.code} sent successfully')
                return True
            except TwilioRestException as e:
                print(e)
            self.sent = timezone.now()
            self.save()
        else:
            print("Twilio credentials are not set")

    def check_verification(self, code):
        if (
            not self.is_code_expired() and
            code == self.code
            # and self.verified == False
        ):
            self.verified = True
            self.save()
        else:
            raise NotAcceptable(
                # ("Your security code is wrong, expired or this phone is verified before."))
                ("Your security code is wrong or expired."))

        return self.verified


class User(AbstractUser):
    username = None
    phone_no = models.OneToOneField(
        PhoneNumber, related_name='user', on_delete=models.CASCADE, null=True, blank=True)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, null=True, blank=True)
    sublevel = models.ForeignKey(
        SubLevel, on_delete=models.CASCADE, null=True, blank=True)
    is_parent = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_no'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return f'{self.full_name()} | {str(self.phone_no)}'

    # def __str__(self):
    #     return self.first_name


@receiver(post_save, sender=User)
def create_parent(sender, instance, *args, **kwargs):
    if instance.is_parent == True:
        try:
            parent = Parent.objects.get(user=instance)
            print(f'{parent} | True')
        except Parent.DoesNotExist:
            Parent.objects.create(user=instance)
            print('created')
            pass


class Parent(models.Model):
    user = models.OneToOneField(
        User, related_name='parent', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Student(models.Model):
    user = models.OneToOneField(
        User, related_name='student', on_delete=models.CASCADE)
    parent = models.ForeignKey(
        Parent,  related_name='student', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user)
