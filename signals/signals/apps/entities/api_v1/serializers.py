from rest_framework import serializers
from ..models import Person, Company
from signals.apps.authentication.api_v1.serializers import UserSerializer

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
