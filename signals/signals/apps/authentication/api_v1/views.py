from rest_framework.exceptions import MethodNotAllowed, NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated

from .. import models
from . import serializers
from signals.libs.permissions import SameUserPermission
from signals.libs.views import APIViewSet

class UserViewSet(APIViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
#    permission_classes = (IsAuthenticated, SameUserPermission)

