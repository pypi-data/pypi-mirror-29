from entity.models import ImageTag
from rest_framework import serializers


class ImageTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageTag
        fields = '__all__'
