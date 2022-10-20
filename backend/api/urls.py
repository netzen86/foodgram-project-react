from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientsViewSet, RecipeCartDownloadView,
                    RecipeCartViewSet, RecipeFavoriteViewSet, RecipeViewSet,
                    SubscribeViewSet, SubscriptionsViewSet, TagsViewSet)

app_name = "api"

router = DefaultRouter()
router.register(r"ingredients", IngredientsViewSet, basename="ingredients")
router.register(r"tags", TagsViewSet, basename="tags")
router.register(r"recipes", RecipeViewSet, basename="recipes")
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
router.register(
    r"users/(?P<user_id>\d+)/subscribe",
    SubscribeViewSet,
    basename="subscribe",
)
router.register(
    r"users/subscriptions",
    SubscriptionsViewSet,
    basename="subscriptions",
)

urlpatterns = [
    path("recipes/download_shopping_cart/", RecipeCartDownloadView.as_view()),
    path("", include(router.urls)),
    path("", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
]
