from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from users.models import User, PhoneNumber


class PhoneNumberAuthBackend(ModelBackend):
    """
    Custom authentication backend to login users using phone number.
    """

    def authenticate(self, request, username=None, password=None):

        try:
            # phone = PhoneNumber.objects.get(phone_no=username)
            user = User.objects.get(phone_no__phone_no=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return
