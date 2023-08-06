from election.models import BallotMeasure
from rest_framework import serializers


class BallotMeasureSerializer(serializers.ModelSerializer):
    class Meta:
        model = BallotMeasure
        fields = '__all__'
