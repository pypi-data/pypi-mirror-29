from entity.models import ImageTag
from entity.serializers import ImageTagSerializer

from .base import BaseViewSet


class ImageTagViewSet(BaseViewSet):
    queryset = ImageTag.objects.all()
    serializer_class = ImageTagSerializer
