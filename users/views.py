from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import Payment, User
from users.permissions import IsOwner
from users.serializers import PaymentSerializer, UserSerializer
from users.services import create_price, create_product, create_session


class UserCreateAPIView(generics.CreateAPIView):
    """Model CreateAPIView for User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(generics.ListAPIView):
    """Model ListAPIView for User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveAPIView(generics.RetrieveAPIView):
    """Model RetrieveAPIView for User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    """Model UpdateAPIView for User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]


class UserDeleteAPIView(generics.DestroyAPIView):
    """Model DestroyAPIView for User."""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner, IsAuthenticated]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Model CreateAPIView for Payment."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product_name = (
            payment.course.title if payment.course.title else payment.lesson.title
        )
        product_id = create_product(product_name)
        price = create_price(payment.amount, product_id)
        session_id, session_url = create_session(price)
        payment.product_id = product_id
        payment.session_id = session_id
        payment.url = session_url
        payment.save()


class PaymentListAPIView(generics.ListAPIView):
    """Model ListAPIView for Payment."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["course", "lesson", "method"]
    ordering_fields = ["created_at"]


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Model RetrieveAPIView for Payment."""

    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
