from collections import OrderedDict
import datetime

from django.contrib.auth.models import AnonymousUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class AuditedModelSerializerString(serializers.ModelSerializer):
    create_by = serializers.StringRelatedField(many=True)
    update_by = serializers.StringRelatedField(many=True)
    common_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

class AuditedModelSerializerIds(serializers.ModelSerializer):
    # Field create_by is a Foreign Key. So with this serialization we will
    # obtain a list of ids.
    create_by = serializers.PrimaryKeyRelatedField(required=False, read_only=True)
    update_by = serializers.PrimaryKeyRelatedField(required=False, read_only=True)

class AuditedModelSerializer(serializers.ModelSerializer):
    common_fields = ['created_by', 'created_at', 'updated_by', 'updated_at']

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
