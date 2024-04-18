from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, generics

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Model ViewSet for User."""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentCreateAPIView(generics.CreateAPIView):
    """Model CreateAPIView for Payment."""
    serializer_class = PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    """Model ListAPIView for Payment."""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['course', 'lesson', 'method']
    ordering_fields = ['created_at']


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Model RetrieveAPIView for Payment."""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
