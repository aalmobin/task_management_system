from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from rest_framework import filters as drf_filters
from rest_framework import generics, permissions, viewsets, response, status
from rest_framework.decorators import action

from . import serializers
from . import models
from . import paginations
from . import permissions as custom_permissions

USER = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = USER.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = serializers.RegisterSerializer


class TaskFilter(filters.FilterSet):
    is_completed = filters.CharFilter(method="filter_by_is_completed")
    due_date = filters.DateTimeFilter(field_name="due_date")
    assigned_to_user = filters.CharFilter(method="filter_by_assigned_to_user")

    def filter_by_is_completed(self, queryset, name, value):
        if value is None:
            return queryset
        try:
            if value == "true":
                return queryset.filter(is_completed=True)
            elif value == "false":
                return queryset.filter(is_completed=False)
        except:
            return queryset.none()

    def filter_by_assigned_to_user(self, queryset, name, value):
        if value is None:
            return queryset
        try:
            return queryset.filter(assignee=value)
        except:
            return queryset.none()

    class Meta:
        model = models.Task
        fields = [
            "is_completed",
            "due_date",
        ]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = models.Task.objects.all()
    serializer_class = serializers.TaskSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        custom_permissions.IsAdminOrOwnerOrManagerOrReadOnly,
    ]
    pagination_class = paginations.TaskPagination
    filterset_class = TaskFilter
    filter_backends = [
        filters.DjangoFilterBackend,
        drf_filters.SearchFilter,
        drf_filters.OrderingFilter,
    ]
    ordering_fields = [
        "due_date",
    ]

    def perform_create(self, serializer):
        """Set the task creator to the logged in user"""
        serializer.save(creator=self.request.user)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=(
            permissions.IsAuthenticatedOrReadOnly,
            custom_permissions.IsAdminOrOwnerOrManagerOrReadOnly,
        ),
    )
    def add_assignee_in_task(self, request, pk=None, *args, **kwargs):
        obj = self.get_object()
        assignee_ids = request.data.get("assignee_ids")

        for assignee_id in assignee_ids:
            try:
                assigne = USER.objects.get(id=assignee_id)
                obj.assignee.add(assigne)
            except:
                pass
        data = {"message": "assignee added successfully"}
        return response.Response(data=data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=(
            permissions.IsAuthenticatedOrReadOnly,
            custom_permissions.IsAdminOrOwnerOrManagerOrReadOnly,
        ),
    )
    def remove_assignee_in_task(self, request, pk=None, *args, **kwargs):
        obj = self.get_object()
        assignee_ids = request.data.get("assignee_ids")

        for assignee_id in assignee_ids:
            try:
                assigne = USER.objects.get(id=assignee_id)
                obj.assignee.remove(assigne)
            except:
                pass
        data = {"message": "assignee removed successfully"}
        return response.Response(data=data, status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=["post"],
        permission_classes=(
            permissions.IsAuthenticatedOrReadOnly,
            custom_permissions.IsAdminOrOwnerOrManagerOrReadOnly,
        ),
    )
    def change_is_completed(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_completed = request.data.get("is_completed")
        task.save()
        return response.Response({"success": True}, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        custom_permissions.IsAdminOrOwnerOrManagerOrReadOnly,
    ]

    def perform_create(self, serializer):
        """Set the comment creator to the logged in user"""
        serializer.save(creator=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = USER.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [
        custom_permissions.IsAdminOrManager,
    ]
