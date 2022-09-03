import django.contrib.auth.password_validation as validators
from django.core import exceptions
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator
from djoser.serializers import UserCreateSerializer
from djoser.serializers import UserSerializer

from .models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        if (
            'request' not in self.context or
            self.context['request'].user.is_anonymous
        ):
            return False
        return Follow.objects.filter(
            author=obj, user=self.context['request'].user
        ).exists()

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

class FollowListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipes.count', read_only=True
    )

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        return Follow.objects.filter(
            author=obj, user=self.context['request'].user
        ).exists()

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


class FollowCreateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=CurrentUserDefault(),
        ),
    author = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'author')
        