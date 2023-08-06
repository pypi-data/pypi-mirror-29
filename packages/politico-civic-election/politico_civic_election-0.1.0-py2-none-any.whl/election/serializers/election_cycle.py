from election.models import ElectionCycle
from rest_framework import serializers


class ElectionCycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionCycle
        fields = '__all__'
