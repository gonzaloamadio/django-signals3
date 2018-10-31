from entities import models
from . import serializers
from signals.libs.views import APIViewSet

class PersonViewSet(APIViewSet):
    """
        A class based view for managing Person
    """
    queryset = models.Person.objects.all()
    serializer_class = serializers.PersonSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class CompanyViewSet(APIViewSet):
    queryset = models.Company.objects.all()
    serializer_class = serializers.CompanySerializer

