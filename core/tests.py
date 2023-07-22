from django.http import response
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from core.models import Task, Comment


class TaskAPITestCase(APITestCase):
    def create_task(self):
        sample_task = {
            "name": "first  task",
            "description": "Test",
            "due_date": "2023-07-28T05:07:42Z",
        }
        response = self.client.post("/api/v1/tasks/", sample_task)
        return response

    def create_comment(self):
        self.authenticate()
        task = self.create_task()
        comment = {
            "text": "something",
            "task": task.data["id"],
        }
        response = self.client.post("/api/v1/comments/", comment)
        return response

    def authenticate(self):
        self.client.post(
            reverse("register-user"),
            {
                "username": "test",
                "email": "email@gmail.com",
                "password": "a2mkUn12345",
                "password2": "a2mkUn12345",
                "first_name": "test",
                "last_name": "test_2",
            },
        )

        response = self.client.post(
            reverse("token_obtain_pair"),
            {
                "username": "test",
                "password": "a2mkUn12345",
            },
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")


class TestListCreateRetrieveUpdateDeleteTasks(TaskAPITestCase):
    def test_should_not_create_task_with_no_auth(self):
        response = self.create_task()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_should_create_task(self):
        previous_task_count = Task.objects.all().count()
        self.authenticate()

        response = self.create_task()
        self.assertEqual(Task.objects.all().count(), previous_task_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "first  task")
        self.assertEqual(response.data["description"], "Test")

    def test_retrieves_all_tasks(self):
        self.authenticate()
        response = self.client.get("/api/v1/tasks/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data["results"], list)

        self.create_task()
        res = self.client.get("/api/v1/tasks/")
        self.assertIsInstance(res.data["count"], int)
        self.assertEqual(res.data["count"], 1)

    def test_retrieves_one_item(self):
        self.authenticate()
        response = self.create_task()
        res = self.client.get(f"/api/v1/tasks/{response.data['id']}/")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        task = Task.objects.get(id=response.data["id"])

        self.assertEqual(task.name, res.data["name"])

    def test_updates_one_item(self):
        self.authenticate()
        response = self.create_task()

        res = self.client.patch(
            f"/api/v1/tasks/{response.data['id']}/",
            {"name": "New one", "is_completed": True},
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        updated_task = Task.objects.get(id=response.data["id"])
        self.assertEqual(updated_task.is_completed, True)
        self.assertEqual(updated_task.name, "New one")

    def test_deletes_one_item(self):
        self.authenticate()
        res = self.create_task()
        prev_db_count = Task.objects.all().count()

        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)

        response = self.client.delete(f"/api/v1/tasks/{res.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Task.objects.all().count(), 0)


class TestListCreateRetrieveUpdateDeleteComments(TaskAPITestCase):
    def test_should_create_comment(self):
        response = self.create_comment()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "something")

    def test_retrieves_all_comments(self):
        self.create_comment()
        res = self.client.get("/api/v1/comments/")
        self.assertIsInstance(res.data["count"], int)
        self.assertEqual(res.data["count"], 1)

    def test_retrieves_one_item(self):
        response = self.create_comment()
        res = self.client.get(f"/api/v1/comments/{response.data['id']}/")

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        comment = Comment.objects.get(id=response.data["id"])

        self.assertEqual(comment.text, res.data["text"])

    def test_updates_one_item(self):
        response = self.create_comment()

        res = self.client.patch(
            f"/api/v1/comments/{response.data['id']}/",
            {"text": "New text"},
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        updated_comment = Comment.objects.get(id=response.data["id"])
        self.assertEqual(updated_comment.text, "New text")

    def test_deletes_one_item(self):
        response = self.create_comment()
        prev_db_count = Comment.objects.all().count()

        self.assertGreater(prev_db_count, 0)
        self.assertEqual(prev_db_count, 1)

        response = self.client.delete(f"/api/v1/comments/{response.data['id']}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Comment.objects.all().count(), 0)
