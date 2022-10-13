from rest_framework import mixins, viewsets


class ListModelViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    pass


class CreateDestroyModelViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass