from election.models import Candidate
from election.serializers import CandidateSerializer

from .base import BaseViewSet


class CandidateViewSet(BaseViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
