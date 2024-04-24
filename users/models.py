from django.contrib.auth.models import AbstractUser
from django.db import models

from config import settings


class User(AbstractUser):
    """Model definition for users in the system"""

    username = None
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, verbose_name="телефон", **settings.NULLABLE)
    city = models.CharField(max_length=35, verbose_name="город", **settings.NULLABLE)
    avatar = models.ImageField(
        upload_to="users/avatars", verbose_name="аватар", **settings.NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.phone}"

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Payment(models.Model):
    """Model definition for Payment."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    course = models.ForeignKey(
        "lms.Course",
        on_delete=models.CASCADE,
        related_name="payments",
        **settings.NULLABLE,
    )
    lesson = models.ForeignKey(
        "lms.Lesson",
        on_delete=models.CASCADE,
        related_name="payments",
        **settings.NULLABLE,
    )
    amount = models.FloatField(verbose_name="сумма")
    method = models.CharField(
        max_length=35,
        choices=[("transfer", "перевод"), ("cash", "наличные")],
        verbose_name="метод оплаты",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="дата создания")

    def __str__(self):
        return f"{self.user} - {self.course if self.course else self.lesson}"

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"
