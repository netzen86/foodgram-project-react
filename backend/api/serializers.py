import base64

from django.core.files.base import ContentFile
from django.db.models import Count
from djoser import serializers
from foodgram.models import Ingredients, IngredientsRecipe, Recipe, Tags
from rest_framework import serializers
from users.models import CustomUser as User


class Base64ImageField(serializers.ImageField):
    """Преобразованние текста в файл картинки"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj: User) -> bool:
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
        return obj.following.filter(id=user.id).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователя."""

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def to_representation(self, obj: User):
        self.fields.pop('password')
        return super().to_representation(obj)


class RecipeCompactSerializer(serializers.ModelSerializer):
    """Сериализатор рецепта для пользователя."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscribedSerializer(UserSerializer):
    """Сериализатор подписки на пользователя."""
    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'recipes',
            'recipes_count',
            'is_subscribed',
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return RecipeCompactSerializer(recipes, many=True).data

    @staticmethod
    def get_recipes_count(obj: User) -> int:
        return obj.recipes.aggregate(Count('id'))['id__count']


class IngredientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""

    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class TagsSerializer(serializers.ModelSerializer):
    """Сериализатор тэгов."""

    class Meta:
        model = Tags
        fields = ('id', 'name', 'color', 'slug')


class IngredientsRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиент рецепт для чтения."""

    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'amount', 'measurement_unit', 'name')

    id = serializers.ReadOnlyField(source='ingredients_id.id')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients_id.measurement_unit'
    )
    name = serializers.ReadOnlyField(source='ingredients_id.name')


class IngredientsRecipeSerializerWrite(IngredientsRecipeSerializer):
    """Сериализатор ингридиент рецепт для записи."""
    class Meta:
        model = IngredientsRecipe
        fields = ('id', 'amount')

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredients.objects.all(),
        required=True,
    )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецепт для чтения."""
    class Meta:
        model = Recipe
        fields = (
            'author',
            'cooking_time',
            'id',
            'image',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'tags',
            'text',
        )

    tags = TagsSerializer(
        many=True,
        required=True,
    )
    author = UserSerializer(
        required=True,
    )
    ingredients = IngredientsRecipeSerializer(
        many=True,
        required=True,
        source='IngredientsRecipe',
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj: Recipe) -> bool:
        user = self.context.get('request').user

        if not user.is_authenticated:
            return False

        return user.favorite.filter(id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj: Recipe) -> bool:
        user = self.context.get('request').user

        if not user.is_authenticated:
            return False

        return user.cart.filter(id=obj.id).exists()


class RecipeCreateSerializer(RecipeSerializer):
    """Сериализатор рецепт для записи."""

    class Meta:
        model = Recipe
        fields = (
            'cooking_time',
            'image',
            'ingredients',
            'name',
            'tags',
            'text',
        )

    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tags.objects.all(),
        many=True,
        required=True,
    )
    ingredients = IngredientsRecipeSerializerWrite(
        many=True,
        required=True,
    )
    image = Base64ImageField(required=True)

    def process_data(self, validated_data, instance=None):
        validated_data['author'] = self.context.get('request').user
        try:
            tags = validated_data.pop('tags')
        except KeyError:
            tags = []
        try:
            ingredients = validated_data.pop('ingredients')
        except KeyError:
            ingredients = []
        if instance is None:
            recipe = Recipe.objects.create(**validated_data)
        else:
            recipe = instance
            for attr, value in validated_data.items():
                setattr(recipe, attr, value)
        if tags:
            recipe.tags.clear()
            for tag_item in tags:
                recipe.tags.add(tag_item)
        if ingredients:
            recipe.ingredients.clear()
            for ingredient_item in ingredients:
                recipe.ingredients.add(
                    ingredient_item['id'],
                    through_defaults={'amount': ingredient_item['amount']},
                )
        recipe.save()

        return recipe

    def create(self, validated_data):
        return self.process_data(validated_data)

    def update(self, instance, validated_data):
        return self.process_data(validated_data, instance)

    def to_representation(self, obj: Recipe):
        serializer = RecipeSerializer(instance=obj, context=self.context)
        return serializer.data
