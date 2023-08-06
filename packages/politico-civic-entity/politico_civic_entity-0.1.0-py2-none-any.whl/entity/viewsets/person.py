from entity.models import Person
from entity.serializers import PersonSerializer

from .base import BaseViewSet


class PersonViewSet(BaseViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
