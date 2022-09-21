from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet, RecipeViewSet, TagsViewSet, UserViewSet

app_name = "api"

router = DefaultRouter()
# router.register(r"users", UserViewSet, basename='users')
router.register(r'ingredients', IngredientsViewSet, basename='ingredients')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
# router.register(
#     r'titles/(?P<url_title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews'
# )
# router.register(
#     r'titles/(?P<url_title_id>\d+)/reviews/(?P<url_review_id>\d+)/comments',
#     CommentsViewSet,
#     basename='comments'
# )

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
]
