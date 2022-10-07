from rest_framework.serializers import ModelSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Course, Lesson
from users.models import User


class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class UserSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
