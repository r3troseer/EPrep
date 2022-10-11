from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView
from django.http import request
from .models import Course, Lesson
from users.models import User, PhoneNumber
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import SubjectSerializer, TopicSerializer, UserSerializer
# from otp.serializers import OtpSerializer
from users.serializers import UserRegisterSerializer, UserLoginSerializer, PhoneNumberSerializer, VerifyPhoneNumberSerialzier


@api_view(['GET'])
def getSubjects(request):
    user = request.user
    print(user)
    sublevel = user.sublevel
    print(sublevel)
    subjects = Course.objects.filter(sublevel__name=sublevel)
    serializer = SubjectSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTopics(request):
    topics = Lesson.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTopic(request, pk):
    topics = Lesson.objects.get(id=pk)
    serializer = TopicSerializer(topics, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def getUser(request):
    user = User.objects.all
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def createTopic(request):
    data = request.data
    topic = Lesson.objects.create(
        name=data['name'],
        subject=data['subject'],
        body=data['body']
    )
    serializer = TopicSerializer(topic, many=False)
    return Response(serializer.data)


# @api_view(['GET'])
# def verify_view(request):
#     data = request.data
#     serializer = OtpSerializer
#     return Response(serializer.data)


class PhoneNumberView(generics.CreateAPIView):
    queryset = PhoneNumber.objects.all()
    serializer_class = PhoneNumberSerializer

    def perform_create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        response_data = ''
        phone_no = request.data.get('phone_no', None)
        print('okay')

        if phone_no:
            res = SendOrResendSMSAPIView.as_view()(request, *args, **kwargs)

            if res.status_code == 200:
                response_data = {"detail": (
                    "Verification e-mail and SMS sent.")}

        return Response(response_data,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    # def create(self, request):
    #     serializer = self.get_serializer(data=request.data)

    #     if serializer.is_valid():
    #         phone_number = str(serializer.validated_data[phone_number])

    #         phone_number.send_confirmation
    #         return Response(status=status.HTTP_200_OK)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserRegisterView(RegisterView):


class UserRegisterationView(RegisterView):
    """
    Register new users using phone number and password.
    """
    serializer_class = UserRegisterSerializer

    def get_serializer_context(self):
        phone_no = self.request.session.get('mobile', None)
        context = super(UserRegisterationView, self).get_serializer_context()
        context.update({
            "phone_no": phone_no
            # extra data
        })
        return context


class UserLoginAPIView(LoginView):
    """
    Authenticate existing users using phone number and password.
    """
    serializer_class = UserLoginSerializer


class SendOrResendSMSAPIView(GenericAPIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """
    serializer_class = PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Send OTP

            phone_no = '+234'+str(serializer.validated_data['phone_no'])
            # del request.session['phone']
            # request.session.modified = True
            self.request.session['mobile'] = phone_no
            phon = self.request.session['mobile']
            print(f'{phon} test')
            phone = PhoneNumber.objects.filter(
                phone_no=phone_no, verified=False)
            if phone.exists():
                print(phone)
                sms_verification = phone.first()
                print(sms_verification)
                sms_verification.send_confirmation()
            else:
                sms_verification = PhoneNumber.objects.create(
                    phone_no=phone_no, verified=False)
                print(sms_verification)
                sms_verification.send_confirmation()
            return Response(status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneNumberAPIView(GenericAPIView):
    """
    Check if submitted phone number and OTP matches and phone number.
    """
    serializer_class = VerifyPhoneNumberSerialzier

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            phone_no = self.request.session['mobile']

            # pho=request.session['phone']
            print(f'{phone_no} test')
            # phone_no = validated_data.get('phone_no')
            otp = (serializer.validated_data['otp'])
            print(otp)

            queryset = PhoneNumber.objects.get(phone_no=phone_no)

            queryset.check_verification(code=otp)
            message = {'detail': ('Phone number successfully verified.')}
            return Response(message, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
