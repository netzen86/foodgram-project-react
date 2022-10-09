from json import dumps

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
# from django.db.models import Avg
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
# LimitOffsetPagination,
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from foodgram.models import Ingredients, Recipe, Tags

from backend import settings

from .permissions import AdminOrReadOnly, OnlyAdmin, OnlyAdminCanGiveRole
from .serializers import (IngredientsSerializer, RecipeSerializer,
                          RecipeSerializerWrite, TagsSerializer,
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
    permission_classes = (AdminOrReadOnly,)
    lookup_field = "id"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = None


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для работы с тэгами."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = "id"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для работы с тэгами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (AdminOrReadOnly,)
    lookup_field = "id"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_serializer_class(self):
        if self.action in (
            "create",
            "partial_update",
            "update",
        ):
            return RecipeSerializerWrite
        return RecipeSerializer


@api_view(["POST"])
@permission_classes([AllowAny])
def register_view(request):
    """
    Функция создает пользователя и
    отправляет ему на почту код подтверждения.
    """
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    username = serializer.validated_data["username"]
    user = get_object_or_404(User, username=username)
    confirmation_code = default_token_generator.make_token(user)
    body = {"username": username, "confirmation_code": confirmation_code}
    json_body = dumps(body)
    send_mail(
        subject="Подтверждение регистрации на сайте yamDB",
        message=(
            f"Добрый день, {username}!\n"
            f"Для подтверждения регистрации отправьте POST "
            f"запрос на http://{settings.DOMAIN}/api/v1/auth/token/ "
            f"в теле запроса передайте:\n"
            f"{json_body}"
        ),
        from_email=f"{settings.CONFIRM_EMAIL}",
        recipient_list=[request.data["email"]],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


def token_view(request):
    """Получение токена при POST-запросе."""
    pass


class UserViewSet(viewsets.ModelViewSet):
    """
    Вью-сет для работы с пользователем.
    Только для админа.
    """

    permission_classes = (OnlyAdmin,)
    serializer_class = UserSerializer
    queryset = User.objects.all()
    lookup_field = "username"
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    pagination_class = PageNumberPagination

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated, OnlyAdminCanGiveRole],
    )
    def me(self, request):
        username = request.user.username
        user = get_object_or_404(User, username=username)
        if request.method == "PATCH":
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
