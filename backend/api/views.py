import io
from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from django.http import FileResponse
# from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from foodgram.models import Ingredients, Recipe, Tags
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, status, views, viewsets
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .helpers import get_unique_recipe_ingredients
from .mixins import CreateDestroyModelViewSet, ListModelViewSet
from .pagination import PageNumberLimitPagination
from .permissions import IsAdminOrAuthorOrReadOnly
from .serializers import (IngredientsSerializer, RecipeCompactSerializer,
                          RecipeCreateSerializer, RecipeSerializer,
                          TagsSerializer, UserSubscribedSerializer)

User = get_user_model()


class SubscriptionsViewSet(ListModelViewSet):
    """Представление для подписок."""

    serializer_class = UserSubscribedSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PageNumberLimitPagination

    def get_queryset(self):
        return self.request.user.follower.all()


class SwitchOnOffViewSet(CreateDestroyModelViewSet):
    model_class = models.Model
    router_pk = "id"
    error_text_create = "Невозможно добавить запись"
    error_text_destroy = "Невозможно удалить запись"
    permission_classes = (permissions.IsAuthenticated,)

    # def get_object(self) -> models.Model:
    def get_object(self):
        return self.queryset.get(
            id=self.kwargs.get(self.router_pk)
        )
        # queryset = self.get_queryset()
        # return get_object_or_404(
        #     queryset,
        #     pk=self.kwargs.get(self.router_pk)
        # )
        # return get_object_or_404(
        #     self.model_class,
        #     pk=self.kwargs.get(self.router_pk)
        # )

    def is_on(self) -> bool:
        pass

    @staticmethod
    def error(text: str) -> Response:
        return Response(
            {
                "errors": text,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def create(self, request, *args, **kwargs):
        if self.is_on():
            return self.error(self.error_text_create)
        obj = self.get_object()
        serializer = self.get_serializer(instance=obj)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not self.is_on():
            return self.error(self.error_text_destroy)
        return super().destroy(request, *args, **kwargs)


class RecipeFavoriteViewSet(SwitchOnOffViewSet):
    """Сериализатор для добавления в избранное"""

    model_class = Recipe
    serializer_class = RecipeCompactSerializer
    router_pk = "recipe_id"
    error_text_create = "Рецепт уже добавлен в список избранное"
    error_text_destroy = "Рецепта нет в списке избранного"

    def is_on(self) -> bool:
        recipe = self.get_object()
        return self.request.user.favorite.filter(id=recipe.id).exists()

    def perform_create(self, serializer: RecipeCompactSerializer):
        recipe = self.get_object()
        self.request.user.favorite.add(recipe)
        self.request.user.save()

    def perform_destroy(self, instance: Recipe):
        self.request.user.favorite.remove(instance)
        self.request.user.save()


class RecipeCartViewSet(SwitchOnOffViewSet):
    """Представление для добавления в список покупок"""

    model_class = Recipe
    serializer_class = RecipeCompactSerializer
    router_pk = "recipe_id"
    error_text_create = "Рецепт уже добавлен список покупок"
    error_text_destroy = "Рецепта нет в списке покупок"

    def is_on(self) -> bool:
        recipe = self.get_object()

        return self.request.user.cart.filter(id=recipe.id).exists()

    def perform_create(self, serializer: RecipeCompactSerializer):
        recipe = self.get_object()

        self.request.user.cart.add(recipe)
        self.request.user.save()

    def perform_destroy(self, instance: Recipe):
        self.request.user.cart.remove(instance)
        self.request.user.save()


class SubscribeViewSet(SwitchOnOffViewSet):
    """Представление для подписки"""

    model_class = User
    serializer_class = UserSubscribedSerializer
    router_pk = 'user_id'
    error_text_create = "Подписка уже существует"
    error_text_destroy = "Подписки не существует"

    def is_on(self) -> bool:
        user = self.get_object()
        return self.request.user.follower.filter(id=user.id).exists()

    def create(self, request, *args, **kwargs):
        user = self.get_object()
        if self.request.user.id == user.id:
            return self.error("Невозможно подписаться на самого себя")
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer: UserSubscribedSerializer):
        user = self.get_object()

        self.request.user.follower.add(user)
        self.request.user.save()

    def perform_destroy(self, instance: User):
        self.request.user.follower.remove(instance)
        self.request.user.save()


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для работы с ингридиентами."""

    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление для работы с тэгами."""

    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Представление для работы с тэгами."""

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberLimitPagination
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    lookup_field = "id"
    search_fields = ("name",)

    def get_serializer_class(self):
        if self.action in (
            "create",
            "partial_update",
            "update",
        ):
            return RecipeCreateSerializer
        return RecipeSerializer


class SaveCartView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)
    font_path = "./static/fonts/JetBrainsMono-Medium.ttf"
    filename = "file.pdf"

    def get_text_lines(self):
        pass

    def get(self, request):
        buffer = io.BytesIO()
        pdfmetrics.registerFont(TTFont("Font", self.font_path))
        page = canvas.Canvas(buffer, pagesize=A4)
        page.setFont("Font", 14)
        text = page.beginText()
        text.setTextOrigin(80, 750)
        text.textLine(f'СПИСОК ПОКУПОК {datetime.date(datetime.now())}.')
        for text_line in self.get_text_lines():
            text.textLine(text=text_line)
        page.drawText(text)
        page.showPage()
        page.save()
        buffer.seek(0)
        return FileResponse(
            buffer,
            as_attachment=True,
            filename=self.filename,
        )


class RecipeCartDownloadView(SaveCartView):
    filename = f'Список покупок {datetime.date(datetime.now())}.pdf'

    def get_text_lines(self):
        recipes = self.request.user.cart.all()
        unique_recipe_ingredients = get_unique_recipe_ingredients(recipes)
        text_lines = []

        for ingredient in unique_recipe_ingredients.values():
            text_lines.append(
                f"{ingredient['name']} ({ingredient['unit']}) "
                f"— {ingredient['amount']}"
            )

        return text_lines
