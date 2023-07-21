from rest_framework.pagination import LimitOffsetPagination


class TaskPagination(LimitOffsetPagination):
    default_limit = 10
