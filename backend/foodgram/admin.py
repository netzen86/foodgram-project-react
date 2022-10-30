from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Ingredients, IngredientsRecipe, Recipe, Tags, TagsRecipe


class IngredientsAdmin(admin.ModelAdmin):
    """Админка для ингридиентов"""
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class IngredientsRecipeAdmin(admin.ModelAdmin):
    """Админка для ингридиентов и рецептов"""
    list_display = ('id', 'recipe_id', 'ingredients_id', 'amount')
    search_fields = ('recipe_id',)
    list_filter = ('recipe_id',)
    empty_value_display = '-пусто-'


class RecipeAdmin(admin.ModelAdmin):
    """Админка для рецептов"""
    list_display = (
        'id',
        'author',
        'name',
        'preview_image',
        'text',
        'cooking_time',
    )
    search_fields = ('name', 'text')
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = '-пусто-'
    readonly_fields = ('favorited', 'preview_image',)

    def favorited(self, instance: Recipe) -> int:
        return instance.users_favorited.count()

    favorited.short_description = 'Общее число добавлений рецепта в избранное'

    def preview_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width=100>')

    preview_image.short_description = "Миниатюра"


class TagsAdmin(admin.ModelAdmin):
    """Админка для тэгов"""
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class TagsRecipeAdmin(admin.ModelAdmin):
    """Админка для тэгов и рецептов"""
    list_display = ('id', 'recipe', 'tag')
    search_fields = ('recipe',)
    list_filter = ('tag',)
    empty_value_display = '-пусто-'


admin.site.register(Ingredients, IngredientsAdmin)
admin.site.register(IngredientsRecipe, IngredientsRecipeAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(TagsRecipe, TagsRecipeAdmin)
