from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, generics
from rest_framework import viewsets, mixins
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from djoser.serializers import PasswordSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from djoser.serializers import UserCreateSerializer, UserSerializer

from .models import User, Follow
from .serializers import FollowListSerializer, FollowCreateSerializer, UserSerializer


class SubscriptionsView(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FollowListSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(following__user=user)


class SubscriptionsViewSet(viewsets.ModelViewSet):

    @action(
        detail=True,
        permission_classes=[permissions.IsAuthenticated],
        methods=['POST']
    )
    def subscribe(self, request, **kwargs):
        id = kwargs.get('pk')
        user = self.request.user
        author = get_object_or_404(User, id=id)
        data = {'user': user.id, 'author': id}
        serializer = FollowCreateSerializer(
            data=data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        follow = Follow.objects.create(user=user, author=author)
        serializer = FollowCreateSerializer(
            follow, context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, **kwargs):
        id = kwargs.get('pk')
        user = self.request.user
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.filter(user=user, author=author)
        if follow.exists():
            follow.delete()
            return Response(
                {'detail': '???? ???????????????????? ???? ????????????'},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {'detail': '???? ???? ???????? ?????????????????? ???? ?????????????? ????????????'},
            status=status.HTTP_400_BAD_REQUEST
        )
