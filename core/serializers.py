from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Task, Comment


USER = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=USER.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = USER
        fields = (
            "username",
            "password",
            "password2",
            "email",
            "first_name",
            "last_name",
        )
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )

        return attrs

    def create(self, validated_data):
        user = USER.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )

        user.set_password(validated_data["password"])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    created_tasks = serializers.SerializerMethodField()
    assigned_tasks = serializers.SerializerMethodField()

    class Meta:
        model = USER
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "assigned_tasks",
            "created_tasks",
        ]

    def get_assigned_tasks(self, obj):
        qs = Task.objects.filter(assignee=obj.id)
        return FlatTaskSerializer(qs, many=True).data

    def get_created_tasks(self, obj):
        return FlatTaskSerializer(obj.tasks.all(), many=True).data


class TaskUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
        ]


class TaskSerializer(serializers.ModelSerializer):
    all_assignee = serializers.SerializerMethodField()
    all_comments = serializers.SerializerMethodField()
    creator_info = serializers.SerializerMethodField()

    class Meta:
        model = Task
        exclude = [
            "creator",
        ]
        extra_kwargs = {
            "assignee": {"write_only": True},
        }

    def get_all_assignee(self, obj):
        return TaskUserSerializer(obj.assignee, many=True).data

    def get_all_comments(self, obj):
        return CommentSerializer(obj.task_comments.all(), many=True).data

    def get_creator_info(self, obj):
        return TaskUserSerializer(obj.creator, many=False).data


class FlatTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        exclude = [
            "assignee",
        ]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = [
            "creator",
        ]
