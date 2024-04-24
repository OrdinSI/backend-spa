from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, IsStaff


class CourseViewSet(viewsets.ModelViewSet):
    """ViewSet for Course."""

    serializer_class = CourseSerializer
    queryset = Course.objects.all()

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


class LessonCreateAPIView(generics.CreateAPIView):
    """APIView for creating Lesson."""

    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsStaff]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    """APIView for listing Lesson."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

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


class LessonDeleteAPIView(generics.DestroyAPIView):
    """APIView for deleting Lesson."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, ~IsStaff]
