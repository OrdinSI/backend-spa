from django.urls import path

from users.apps import UsersConfig
from rest_framework import routers

from users.views import UserViewSet, PaymentListAPIView, PaymentRetrieveAPIView, PaymentCreateAPIView

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

app_name = UsersConfig.name


urlpatterns = [
      path('payment/create/', PaymentCreateAPIView.as_view(), name='lesson-create'),
      path('payment/', PaymentListAPIView.as_view(), name='lesson-list'),
      path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='lesson-retrieve'),

] + router.urls
