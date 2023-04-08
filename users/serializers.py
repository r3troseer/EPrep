from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from api.models import Level, Class, Department, Exam, SubLevel
from users.models import User, PhoneNumber
from users.levels import level_set, sub_set
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
    level = serializers.CharField(write_only=True, required=False)
    sub_level = serializers.CharField(write_only=True, required=False)
    is_parent = serializers.BooleanField(required=False)
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


    def custom_signup(self, request, user):
        # self.create_user(user, self.get_cleaned_data_extra())
        phone_no = self.context.get("phone_no")
        print(f'{phone_no} tested')
        phone = PhoneNumber.objects.get(
            phone_no=phone_no, verified=True)
        lev = self.validated_data.get('level')
        sub_level = self.validated_data.get('sub_level')
        try:
            level = Level.objects.get(name=level_set.get(lev))
            sublevel = SubLevel.objects.get(
                name=sub_set.get(lev).get(sub_level))
            user.level = level
            user.sublevel = sublevel
            print(f'{lev, level} and {sub_level, sublevel}')
        except (Level.DoesNotExist, SubLevel.DoesNotExist):
            pass
        parent = self.validated_data.get('is_parent')

        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.phone_no = phone
        user.is_parent = parent

        user.save(update_fields=['first_name',
                  'last_name', 'phone_no', 'level', 'sublevel', 'is_parent'])

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
            # phone = PhoneNumber.objects.get(phone_no=phone_no)
            user = authenticate(
                username=str(phone_no), password=password)
        else:
            raise serializers.ValidationError(
                ("Enter a phone number and password."))

        return user

    def validate(self, validated_data):
        phone_no = validated_data.get('phone_no')
        password = validated_data.get('password')
        print(phone_no, password)

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
        print('login sucessful', phone_no, password)
        return validated_data


class UserDetailsSerializer(serializers.ModelSerializer):
    phone_no = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'full_name',
            'pk',
            'email',
            'phone_no',
        )
        read_only_fields = ('pk', 'phone_no',)


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
