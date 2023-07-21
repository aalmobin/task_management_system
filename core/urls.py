from django.urls import path, include
from rest_framework import routers
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register("tasks", views.TaskViewSet, basename="tasks")
router.register("comments", views.CommentViewSet, basename="comments")
router.register("users", views.UserViewSet, basename="users")

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register-user"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
