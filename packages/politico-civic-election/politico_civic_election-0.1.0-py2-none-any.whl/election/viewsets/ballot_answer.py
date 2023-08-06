from election.models import BallotAnswer
from election.serializers import BallotAnswerSerializer

from .base import BaseViewSet


class BallotAnswerViewSet(BaseViewSet):
    queryset = BallotAnswer.objects.all()
    serializer_class = BallotAnswerSerializer
