from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, UserDetailsView
from django.http import request
from .models import Course, Lesson, Topic
from users.models import User, PhoneNumber, Parent, Student
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import SubjectsSerializer, TopicSerializer, LessonSerializer, ChildSerializer
# from otp.serializers import OtpSerializer
from users.serializers import UserRegisterSerializer, UserLoginSerializer, UserDetailsSerializer, PhoneNumberSerializer, VerifyPhoneNumberSerialzier


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getSubjects(request):
    user = request.user
    print(user)
    sublevel = user.sublevel
    level = user.sublevel.level
    print(sublevel, level)
    subjects = Course.objects.filter(sublevel__name=sublevel)
    serializer = SubjectsSerializer(subjects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getTopics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getLesson(request, pk):
    topics = Lesson.objects.get(id=pk)
    print(topics)
    serializer = LessonSerializer(topics, many=False)
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


class ChildView(generics.CreateAPIView, generics.ListAPIView):
    """
    View children and add to registered parent
    """
    serializer_class = ChildSerializer
    permission_classes = IsAuthenticated

    def get_serializer_context(self):
        parent = self.request.user
        context = super(ChildView, self).get_serializer_context()
        context.update({
            "parent": parent
            # extra data
        })
        return context

    def get_queryset(self):
        user = self.request.user
        parent = Parent.objects.get(user=user)
        queryset = Student.objects.filter(parent=parent)
        return queryset

    def perform_create(self, serializer):
        if serializer.is_valid():
            user = serializer.save()
            return user


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


class Profile(UserDetailsView):
    """
    Reads and updates UserModel fields
    Accepts GET, PUT, PATCH methods.

    Display fields: pk, full_name, email, phone_no
    Read-only fields: pk, phone_no

    Returns UserModel fields.
    """
    serializer_class = UserDetailsSerializer
    permission_classes = [IsAuthenticated]


class SendOrResendSMSAPIView(GenericAPIView):
    """
    Check if submitted phone number is a valid phone number and send OTP.
    """
    serializer_class = PhoneNumberSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Send OTP
            phone_no = str(serializer.validated_data['phone_no'])
            # stores number input in session
            self.request.session['mobile'] = phone_no
            phon = self.request.session['mobile']
            print(f'{phon}, session test')
            phone = PhoneNumber.objects.filter(
                phone_no=phone_no)
            user = User.objects.filter(phone_no__phone_no=phone_no)
            if phone.exists():  # checks if number exists in database
                if user:
                    print(f'{user}, user set')
                    # checks if user exists then returns http code 409
                    message = {'detail': ('Phone number already registered.')}
                    return Response(message, status=status.HTTP_409_CONFLICT)
                else:
                    print(f'{phone}, phone set')
                    # sends verification if user does not exist
                    sms_verification = phone.first()
                    print(f'{sms_verification}, exists')
                    sms_verification.send_confirmation()
                    message = {'detail': ('Verification message sent.')}
            else:
                # create new number and sends verification
                sms_verification = PhoneNumber.objects.create(
                    phone_no=phone_no, verified=False)
                print(f'{sms_verification}, created')
                sms_verification.send_confirmation()
                message = {'detail': ('Verification message sent.')}
            return Response(message, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPhoneNumberAPIView(GenericAPIView):
    """
    Check if submitted phone number and OTP matches.
    """
    serializer_class = VerifyPhoneNumberSerialzier

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # gets number from session
            phone_no = self.request.session['mobile']
            print(f'{phone_no} test')
            otp = (serializer.validated_data['otp'])
            print(otp)
            queryset = PhoneNumber.objects.get(phone_no=phone_no)
            queryset.check_verification(code=otp)
            message = {'detail': ('Phone number successfully verified.')}
            return Response(message, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
