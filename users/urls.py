from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import (
    PaymentCreateAPIView,
    PaymentListAPIView,
    PaymentRetrieveAPIView,
    UserCreateAPIView,
    UserDeleteAPIView,
    UserListAPIView,
    UserRetrieveAPIView,
    UserUpdateAPIView,
)

app_name = UsersConfig.name


urlpatterns = [
    path("payment/create/", PaymentCreateAPIView.as_view(), name="lesson-create"),
    path("payment/", PaymentListAPIView.as_view(), name="lesson-list"),
    path("payment/<int:pk>/", PaymentRetrieveAPIView.as_view(), name="lesson-retrieve"),
    path(
        "token/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="token_obtain_pair",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path("users/create/", UserCreateAPIView.as_view(), name="create-user"),
    path("users/", UserListAPIView.as_view(), name="user-list"),
    path("users/<int:pk>/", UserRetrieveAPIView.as_view(), name="user-retrieve"),
    path("users/delete/<int:pk>/", UserDeleteAPIView.as_view(), name="user-delete"),
    path("users/update/<int:pk>/", UserUpdateAPIView.as_view(), name="user-update"),
]
