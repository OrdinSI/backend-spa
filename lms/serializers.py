from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import DescriptionsValidator


class LessonSerializer(serializers.ModelSerializer):
    """Model Serializer для урока."""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [DescriptionsValidator(field="description")]


class CourseSerializer(serializers.ModelSerializer):
    """Model Serializer для курса."""

    count_lessons = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"
        validators = [DescriptionsValidator(field="description")]

    @staticmethod
    def get_count_lessons(obj):
        return obj.lessons.count()

    @staticmethod
    def get_subscription(obj):
        return obj.subscriptions.exists()
