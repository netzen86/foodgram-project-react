from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet

app_name = "api"

router = DefaultRouter()
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
