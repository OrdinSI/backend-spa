from rest_framework import serializers

from lms.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """Model Serializer для курса."""
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    """Model Serializer для урока."""
    class Meta:
        model = Lesson
        fields = '__all__'
