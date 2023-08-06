from entity.models import Organization
from rest_framework import serializers


class OrganizationSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    classification = serializers.StringRelatedField()

    def get_images(self, obj):
        """Object of images serialized by tag name."""
        return {str(i.tag.name): i.image.url for i in obj.images.all()}

    class Meta:
        model = Organization
        fields = (
            'id',
            'uid',
            'slug',
            'name',
            'identifiers',
            'classification',
            'parent',
            'national_headquarters',
            'founding_date',
            'dissolution_date',
            'images',
            'summary',
            'description',
            'links',
            'created',
            'updated',
        )
