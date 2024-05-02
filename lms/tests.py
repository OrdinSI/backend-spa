from rest_framework.test import APITestCase
from lms.models import Lesson, Course, Subscription
from users.models import User
from rest_framework import status


class LessonTestCase(APITestCase):
    """Test case for Lesson model."""

    def setUp(self):
        self.user = User.objects.create(email="admin@localhost")
        self.course = Course.objects.create(
            title="test", description="test", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="test", description="test", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_list(self):
        response = self.client.get("/lms/lesson/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("count"), 1)

    def test_lesson_detail(self):
        response = self.client.get(f"/lms/lesson/{self.lesson.id}/")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)

    def test_lesson_create(self):
        data = {"title": "test2", "description": "test2",
                "course": self.course.id}
        response = self.client.post("/lms/lesson/create/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_update(self):
        data = {"title": "test3", "description": "test3",
                "course": self.course.id}
        response = self.client.patch(
            f"/lms/lesson/update/{self.lesson.id}/", data)
        data_r = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_r.get("title"), data.get("title"))

    def test_lesson_delete(self):
        response = self.client.delete(f"/lms/lesson/delete/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTestCase(APITestCase):
    """Test case for Subscription model."""

    def setUp(self):
        self.user = User.objects.create(email="admin@localhost")
        self.course = Course.objects.create(
            title="test", description="test", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription_create_and_delete(self):
        data = {"user": self.user.id, "course": self.course.id}
        response_create = self.client.post("/lms/subscribe/", data)
        self.assertEqual(response_create.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)

        self.assertEqual(
            response_create.data["message"], "Вы подписались на курс")

        response_delete = self.client.post("/lms/subscribe/", data)
        self.assertEqual(response_delete.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)

        self.assertEqual(
            response_delete.data["message"], "Вы отписались от курса")
