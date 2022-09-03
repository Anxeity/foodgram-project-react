import rest_framework.permissions
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter, Recipe
from .models import Ingredient, Tag, Favorite, ShoppingCart, IngredientRecipe
from .permissions import IsAuthenticatedOwnerOrReadOnly
from .serializers import (
    IngredientSerializer, TagSerializer, RecipeSerializer,
    FollowRecipeSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = None
    serializer_class = IngredientSerializer
    permission_classes = (AllowAny,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[rest_framework.permissions.IsAuthenticated]
    )
    def favorite(self, request, pk):
        return self.__favorite_shopping(request, pk, Favorite, {
            'recipe_in': 'Рецепт уже в избранном',
            'recipe_not_in': 'Рецепта нет в избранном'
        })
