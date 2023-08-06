from election.models import BallotAnswer
from rest_framework import serializers


class BallotAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotAnswer
        fields = '__all__'
