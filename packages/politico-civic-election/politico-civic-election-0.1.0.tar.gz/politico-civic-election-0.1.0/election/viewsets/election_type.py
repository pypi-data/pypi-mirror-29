from election.models import ElectionType
from election.serializers import ElectionTypeSerializer

from .base import BaseViewSet


class ElectionTypeViewSet(BaseViewSet):
    queryset = ElectionType.objects.all()
    serializer_class = ElectionTypeSerializer
