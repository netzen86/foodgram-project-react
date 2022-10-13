from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipeViewSet,
                    RecipeCartViewSet, RecipeFavoriteViewSet,
                    SubscribeViewSet, SubscriptionsViewSet,
                    TagsViewSet)

app_name = "api"

router = DefaultRouter()
router.register(
    r"ingredients",
    IngredientsViewSet,
    basename="ingredients"
)
router.register(
    r"tags",
    TagsViewSet,
    basename="tags"
)
router.register(
    r"recipes",
    RecipeViewSet,
    basename="recipes"
)
router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    SubscribeViewSet,
    basename="subscribe",
)
router.register(
    "users/subscriptions",
    SubscriptionsViewSet,
    basename="subscriptions",
)
router.register(
    r"recipes/(?P<recipe_id>\d+)/favorite",
    RecipeFavoriteViewSet,
    basename="recipe-favorite",
)
router.register(
    r"recipes/(?P<recipe_id>\d+)/shopping_cart",
    RecipeCartViewSet,
    basename="recipe-cart",
)

urlpatterns = [
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    path("", include(router.urls)),
]
