from json import dumps

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
# from django.db.models import Avg
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
# from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
# LimitOffsetPagination,
# from rest_framework.permissions import AllowAny, IsAuthenticated
#from rest_framework.response import Response
from foodgram.models import Ingredients, Recipe, Tags

from backend import settings

from .permissions import IsAdminOrAuthorOrReadOnly, AdminOrReadOnly, OnlyAdmin, OnlyAdminCanGiveRole
from .serializers import (IngredientsSerializer, RecipeSerializer,
                          RecipeCreateSerializer, TagsSerializer,
                          UserSerializer)

User = get_user_model()


def get_usr(self):
    return get_object_or_404(
        User,
        username=self.request.user,
    )


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для работы с ингридиентами."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    lookup_field = "id"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = None


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для работы с тэгами."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    lookup_field = "id"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для работы с тэгами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    lookup_field = "id"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_serializer_class(self):
        if self.action in (
            "create",
            "partial_update",
            "update",
        ):
            return RecipeCreateSerializer
        return RecipeSerializer
