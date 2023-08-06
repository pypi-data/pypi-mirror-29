from election.models import ElectionDay
from election.serializers import ElectionDaySerializer

from .base import BaseViewSet


class ElectionDayViewSet(BaseViewSet):
    queryset = ElectionDay.objects.all()
    serializer_class = ElectionDaySerializer
