from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from django.utils.translation import ugettext_lazy as _
from .pagination import CustomPagination


class APIPaginatedViewSet(viewsets.GenericViewSet):
    pagination_class = CustomPagination


class APIViewSet(APIPaginatedViewSet,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 mixins.DestroyModelMixin):

    def perform_create(self, serializer):
        """Ensure we have the authorized user for ownership."""
        serializer.save(created_by=self.request.user, updated_by=self.request.user)

    def perform_update(self, serializer):
        """Ensure we have the authorized user for ownership."""
        serializer.save(updated_by=self.request.user)


class APIReadOnlyViewSet(APIPaginatedViewSet,
                         mixins.RetrieveModelMixin,
                         mixins.ListModelMixin):
    pass


class APIListRetrieveUpdateViewSet(APIPaginatedViewSet,
                                   mixins.ListModelMixin,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin):

    def perform_update(self, serializer):
        """Ensure we have the authorized user for ownership."""
        serializer.save(updated_by=self.request.user)
