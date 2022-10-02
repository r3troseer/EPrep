from rest_framework.serializers import ModelSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import Subject, Topic
from users.models import User

class SubjectSerializer(ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class UserSerializer(RegisterSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')