from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class UserRoleChoices(models.IntegerChoices):
    ADMIN = 3
    MANAGER = 2
    TEAM_MEMBER = 1


class User(AbstractUser):

    """
    Possible roles are:
    3: ADMIN
    2: MANAGER
    1: TEAM_MEMBER
    """

    role = models.PositiveSmallIntegerField(
        _("Role"), default=UserRoleChoices.TEAM_MEMBER, choices=UserRoleChoices.choices
    )


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    assignee = models.ManyToManyField("User", blank=True)
    creator = models.ForeignKey("User", on_delete=models.CASCADE, related_name="tasks")
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Comment(models.Model):
    text = models.TextField()
    task = models.ForeignKey(
        "Task", on_delete=models.CASCADE, related_name="task_comments"
    )
    creator = models.ForeignKey("User", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.task.name}-{self.creator.username}"
