from django.contrib import admin

from .models import Ingredients, IngredientsRecipe, Recipe, Tags, TagsRecipe


class IngredientsAdmin(admin.ModelAdmin):
    """Админка для ингридиентов"""
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    # list_filter = ('name',)
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
        'image',
        'text',
        'cooking_time',
        'is_favorited',
        'is_in_shopping_cart',
    )
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


class TagsAdmin(admin.ModelAdmin):
    """Админка для тэгов"""
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('slug',)
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
