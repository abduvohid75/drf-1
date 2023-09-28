from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Course, Lesson, Payments

def check_url(url):
    if url[:23] != 'https://www.youtube.com':
        raise serializers.ValidationError('Ссылка может быть только на youtube.com')

class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    def get_lessons_count(self, obj):
        return obj.lesson_set.count()
    class Meta:
        model = Course
        fields = '__all__'

class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    link = serializers.URLField(validators=[check_url])

    class Meta:
        model = Lesson
        fields = '__all__'

class TokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['email'] = user.email

        return token