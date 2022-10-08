from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from users.models import User, PhoneNumber
from .exceptions import (
    AccountNotRegisteredException,
    InvalidCredentialsException,
    AccountDisabledException,
)

# class PhoneSerializer(serializers):


class UserRegisterSerializer(RegisterSerializer):
    """
    Serializer to register users .
    """
    first_name = serializers.CharField(required=True, write_only=True)
    last_name = serializers.CharField(required=True, write_only=True)
    # phone_no = serializers.CharField(
    #     required=False,
    #     write_only=True,
    # )
    dependent1=serializers.CharField(write_only=True)
    dependent2=serializers.CharField(write_only=True)
    username = None
    email = None

    def validate(self, validated_data):
        # phone_no =  self.context.get("phone_no")

        # if phone_number:
        #     raise serializers.ValidationError(
        #         ("Enter a phone number."))

        if validated_data['password1'] != validated_data['password2']:
            raise serializers.ValidationError(
                ("The two password fields didn't match."))

        return validated_data

    # def get_cleaned_data_extra(self):
    #     return {
    #         'phone_no': self.validated_data.get('phone_no', ''),
    #         'first_name': self.validated_data.get('first_name', ''),
    #         'last_name': self.validated_data.get('last_name', '')
        # }

    # def create_user(self, user, validated_data):
    #     phone_no = validated_data.get("phone_no")
    #     first_name = validated_data.get("first_name")
    #     last_name = validated_data.get("last_name")
    #     phone = PhoneNumber.objects.get(
    #         phone_no=phone_no, verified=True)
    #     user = User.objects.create(
    #         phone_no=phone, first_name=first_name, last_name=last_name)

    #     return user

    def custom_signup(self, request, user):
        # self.create_user(user, self.get_cleaned_data_extra())
        phone_no = self.context.get("phone_no")
        print(f'{phone_no} tested')
        phone = PhoneNumber.objects.get(
            phone_no=phone_no, verified=True)
        dep1= self.validated_data.get('dependent1')
        dep2= self.validated_data.get('dependent2')
        print(f'{dep1} and {dep2} ')
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.phone_no = phone
        user.save(update_fields=['first_name', 'last_name', 'phone_no'])

    # Define transaction.atomic to rollback the save operation in case of error
    # @transaction.atomic
    # def save(self, request):
    #     user = super().save(request)
    #     user.first_name = self.data.get('first_name')
    #     user.last_name = self.data.get('last_name')
    #     user.phone_no = self.data.get('phone_number')
    #     user.save()
    #     return user


...


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer to login users with phone number.
    """
    phone_no = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(
        write_only=True, style={'input_type': 'password'})

    def _validate_phone(self, phone_no, password):
        user = None

        if phone_no and password:
            """
            queries through phonenumber model to get inputed phone number 
            then authenticate
            """
            phone = PhoneNumber.objects.get(phone_no=phone_no)
            user = authenticate(username=phone, password=password)
        else:
            raise serializers.ValidationError(
                ("Enter a phone number and password."))

        return user

    def validate(self, validated_data):
        phone_no = validated_data.get('phone_no')
        password = validated_data.get('password')

        user = None

        user = self._validate_phone(phone_no, password)

        if not user:
            raise InvalidCredentialsException()

        if not user.is_active:
            raise AccountDisabledException()

        # if not user.phone.verified:
        #     raise serializers.ValidationError(
        #         ('Phone number is not verified.'))

        validated_data['user'] = user
        print ('login sucessful')
        return validated_data


class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'phone_number',
        )
        read_only_fields = ('pk', 'email',)


class PhoneNumberSerializer(serializers.ModelSerializer):
    """
    Serializer class to serialize phone number.
    """
    phone_no = serializers.CharField()

    class Meta:
        model = PhoneNumber
        fields = ('phone_no',)


class VerifyPhoneNumberSerialzier(serializers.Serializer):
    """
    Serializer class to verify OTP.
    """
    # phone_no = serializers.CharField()
    otp = serializers.CharField(max_length=settings.TOKEN_LENGTH)

    # def get_phone(self, request):
    #     phone_no = request.session['phone']
    #     return phone_no

    # def validate(self, validated_data):
    #     phone_no = validated_data.get('phone_no')
    #     otp = validated_data.get('otp')

    #     queryset = PhoneNumber.objects.get(phone_no=phone_no)

    #     queryset.check_verification(code=otp)

    #     return validated_data
