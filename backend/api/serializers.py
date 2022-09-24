# from datetime import datetime
import base64
from django.core.files.base import ContentFile
from djoser import serializers
from django.contrib.auth import get_user_model
# from rest_framework.exceptions import ValidationError
# from rest_framework.generics import get_object_or_404
# from rest_framework.relations import SlugRelatedField
# from rest_framework.validators import UniqueTogetherValidator
from foodgram.models import Ingredients, Recipe, Tags
from rest_framework import serializers

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        # Если полученный объект строка, и эта строка
        # начинается с 'data:image'...
        if isinstance(data, str) and data.startswith('data:image'):
            # ...начинаем декодировать изображение из base64.
            # Сначала нужно разделить строку на части.
            format, imgstr = data.split(';base64,')
            # И извлечь расширение файла.
            ext = format.split('/')[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('name', 'measurement_unit',)


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов."""

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""
    ingredients = IngredientsSerializer(read_only=True, many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'cooking_time',
                  'is_favorited', 'is_in_shopping_cart',
                  'ingredients', 'tags')
        read_only_fields = ('author', 'ingredients',)


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания неподтвержденного польлзователя.
    Управление пользователем. Отправка эмэйла."
    """

    class Meta:
        model = User
        fields = ("email", "username")

    def validate_username(self, value):
        """Проверка username !=me"""
        try:
            User.objects.get(username=value).exists()
        except User.DoesNotExist:
            if value.lower() == "me":
                raise serializers.ValidationError(
                    "Использовать имя 'me' в качестве username запрещено."
                )
            return value
        raise serializers.ValidationError("Пользователь существует.")

    def validate_email(self, value):
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            return value
        raise serializers.ValidationError("Пользователь существует.")


class TokenSerializer(serializers.Serializer):
    """Сериализатор для авторизации пользователя."""

    username = serializers.CharField(max_length=255)
    confirmation_code = serializers.CharField(max_length=128)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор управления пользователем."""

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name',
                  'last_name', 'is_subscribed')
