from entity.models import OrganizationClassification
from rest_framework import serializers


class OrganizationClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationClassification
        fields = '__all__'
