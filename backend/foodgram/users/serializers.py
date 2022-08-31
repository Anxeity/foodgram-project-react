import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer

from .models import User, Follow


class UserCreateSerializer(serializers.ModelSerializer):
    """для новых пользователей"""
    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'id'
        )


class UserSerializer(serializers.ModelSerializer):
    """для существующих пользователей"""

    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        """прибавляем поле подписки пользователя на автора."""
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        user = request.user
        following = obj.follower.filter(user=obj, following=user)
        return following.exists()


class FollowListSerializer(serializers.ModelSerializer):
    """для списка избранных авторов"""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source="recipes.count", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "recipes",
            "is_subscribed",
            "recipes_count",
        )
        read_only_fields = fields

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        user = request.user
        following = obj.follower.filter(user=obj, following=user)
        return following.exists()



class FollowCreateSerializer(serializers.ModelSerializer):
    """для подписки на пользователя"""
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ("user", "following",)
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=("user", "following"),
                message="Подписка уже оформлена.",
            )
        ]

    def validate_self_following(self, value):
        user = self.context.get("request").user
        if user == value:
            raise serializers.ValidationError("Нельзя подписаться на себя.")
        return value