from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Course, Lesson, Topic
from users.models import User


class LessonsSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        # fields = '__all__'
        exclude = ['lesson']


class LessonSerializer(LessonsSerializer):
    topic = TopicSerializer(many=True)
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'topic']


class SubjectsSerializer(ModelSerializer):
    lesson = LessonsSerializer(many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'lesson']


class SubjectSerializer(SubjectsSerializer):
    pass


# class TopicSerializer(ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = '__all__'


class UserSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
