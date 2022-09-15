from django.db import models
from users.models import CustomUser as User


class Ingredients(models.Model):
    """Модель ингридиентов"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    ),
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Еденица измерения'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'


class Tags(models.Model):
    name = models.CharField(
        max_length=200,
    ),
    color = models.CharField(
        max_length=7
    ),
    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    image = models.ImageField(
        upload_to='recipe_img/',
        verbose_name='Изображение'
    )
    text = models.TextField(
        verbose_name='Описание'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)'
    )
    is_favorited = models.BooleanField(
        verbose_name='В избранном'
    ),
    is_in_shopping_cart = models.BooleanField(
        verbose_name='В списке покупок'
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='IngredientsRecipe',
        verbose_name='Ингридиенты'
    )
    tags = models.ManyToManyField(
        Tags,
        through='',
        verbose_name='Тэги'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientsRecipe(models.Model):
    """Модель соотношения ингридиентов и рецептов"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredients,
        on_delete=models.CASCADE,
        verbose_name='Ингридиент'
    )
    amount = models.IntegerField(
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Ингридиент-рецепт'
        verbose_name_plural = 'Ингридиенты-рецепты'


class TagsRecipe(models.Model):
    """Модель соотношения тэгов и рецептов"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tags,
        on_delete=models.CASCADE,
        verbose_name='Тэг'
    )

    class Meta:
        verbose_name = 'Тэг-рецепт'
        verbose_name_plural = 'Теги-рецепты'
