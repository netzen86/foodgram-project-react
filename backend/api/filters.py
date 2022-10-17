from foodgram.models import Ingredients, Recipe
from django.db.models import IntegerField, Value

from django_filters import (BaseInFilter, CharFilter,
                            FilterSet, NumberFilter,)


class CharInFilter(BaseInFilter, CharFilter):
    pass


class IngredientFilter(FilterSet):
    class Meta:
        model = Ingredients
        fields = ("name",)

    @staticmethod
    def filter_name(queryset, name, value):
        startswith = queryset.filter(
            **{f"{name}__istartswith": value}
        ).annotate(order=Value(0, IntegerField()))

        contains = (
            queryset.filter(**{f"{name}__icontains": value})
            .exclude(id__in=startswith.values("id"))
            .annotate(order=Value(1, IntegerField()))
        )

        return startswith.union(contains).order_by("order")

    name = CharFilter(field_name="name", method="filter_name")


class RecipeFilter(FilterSet):
    class Meta:
        model = Recipe
        fields = (
            "author",
            "is_favorited",
            "is_in_shopping_cart",
            "tags",
        )

    def filter_is_user_in_list(self, queryset, name, value):
        user = self.request.user

        if not user.is_authenticated:
            return queryset

        kwargs = {f"{name}__in": (user,)}

        if value == 0:
            return queryset.exclude(**kwargs)

        return queryset.filter(**kwargs)

    def filter_tags(self, queryset, name, value):
        tags = self.request.GET.getlist("tags")

        return queryset.filter(**{f"{name}__in": tags}).distinct()

    is_favorited = NumberFilter(
        field_name="users_favorited",
        method="filter_is_user_in_list",
    )
    is_in_shopping_cart = NumberFilter(
        field_name="users_added_to_cart",
        method="filter_is_user_in_list",
    )
    author = CharFilter(
        field_name="author__id",
        lookup_expr="exact",
    )
    tags = CharInFilter(
        field_name="tags__slug",
        method="filter_tags",
    )
