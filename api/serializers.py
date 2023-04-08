from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from users.levels import level_set, sub_set
from .models import Course, Lesson, Topic
from users.models import User, Parent, Student, Level, SubLevel


class LessonsSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name', 'url']


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
        fields = ['id', 'name', 'colour', 'lesson']


class SubjectSerializer(SubjectsSerializer):
    pass


# class TopicSerializer(ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = '__all__'

class LevelSerializer(serializers.Serializer):
    """
    Iterate through level and sublevel id gotten from 
    frontend and return corresponding sublevel object
    """
    level = serializers.CharField(required=False)
    name = serializers.CharField(required=False)

    def _validate_level(self, lev, sub):
        try:
            level = Level.objects.get(name=level_set.get(lev))
            print(level, lev, sub)
            sublevel = SubLevel.objects.get(
                name=sub_set.get(lev).get(sub))
            print(f'{lev, level} and {sub, sublevel}')
        except (Level.DoesNotExist, SubLevel.DoesNotExist):
            raise serializers.ValidationError(
                "level or sublevel does not exist")
        return level, sublevel

    def validate(self, validated_data):
        lev = validated_data.get('level')
        sub_level = validated_data.get('name')
        if lev and sub_level:
            level, sublevel = self._validate_level(lev, sub_level)
            validated_data['level'] = level
            validated_data['name'] = sublevel
        return validated_data


class UserSerializer(ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    sublevel = LevelSerializer()

    class Meta:
        model = User
        fields = ['id','first_name', 'last_name', 'sublevel']

    def validate(self, validated_data):
        # lev = validated_data.get('level')
        sub_level = validated_data.pop('sublevel')
        print(sub_level.get('name'), 'sub')
        sublevel = sub_level.get('name')
        validated_data['sublevel'] = sublevel
        if not sub_level:
            raise serializers.ValidationError("Choose a level and sublevel")
        return validated_data


class ChildSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user']

    def create(self, validated_data):
        parent_data = self.context.get("parent")
        parent = Parent.objects.get(user=parent_data)
        print(parent)
        user_data = validated_data.pop('user')
        print(user_data)
        user = User.objects.create(**user_data)
        print(user)
        student = Student.objects.create(user=user, parent=parent)
        print(student)
        return student
