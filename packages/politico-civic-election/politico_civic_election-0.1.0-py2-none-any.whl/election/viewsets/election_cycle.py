from election.models import ElectionCycle
from election.serializers import ElectionCycleSerializer

from .base import BaseViewSet


class ElectionCycleViewSet(BaseViewSet):
    queryset = ElectionCycle.objects.all()
    serializer_class = ElectionCycleSerializer
