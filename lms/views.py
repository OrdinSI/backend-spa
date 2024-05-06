from django.utils import timezone

from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from lms.models import Course, Lesson, Subscription
from lms.pagination import LmsPaginator
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, IsStaff


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = LmsPaginator

    def get_permissions(self):
        if self.action == "destroy":
            self.permission_classes = [IsAuthenticated, ~IsStaff | IsOwner]
        elif self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsStaff]
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = [IsAuthenticated, IsOwner | IsStaff]
        return super().get_permissions()

    def get_queryset(self):
        """Return the queryset for this view."""
        staff_permission = IsStaff()
        if staff_permission.has_permission(self.request, self):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        course = serializer.save()


class LessonCreateAPIView(generics.CreateAPIView):
    """APIView for creating Lesson."""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsStaff]

    def perform_create(self, serializer):
        instance = serializer.save(owner=self.request.user)
        course = instance.course
        course.updated_at = timezone.now()
        course.save()


class LessonListAPIView(generics.ListAPIView):
    """APIView for listing Lesson."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = LmsPaginator

    def get_queryset(self):
        """Return the queryset for this view."""
        staff_permission = IsStaff()
        if staff_permission.has_permission(self.request, self):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """APIView for retrieving Lesson."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsStaff | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """APIView for updating Lesson."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsStaff | IsOwner]

    def perform_update(self, serializer):
        instance = serializer.save()
        course = instance.course
        course.updated_at = timezone.now()
        course.save()


class LessonDeleteAPIView(generics.DestroyAPIView):
    """APIView for deleting Lesson."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner | ~IsStaff]


class SubscribeAPIView(APIView):
    """APIView for subscribing."""

    def post(self, request, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")

        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(user=user, course=course_item).first()

        if subs_item:
            subs_item.delete()
            message = "Вы отписались от курса"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Вы подписались на курс"
        return Response({"message": message})
