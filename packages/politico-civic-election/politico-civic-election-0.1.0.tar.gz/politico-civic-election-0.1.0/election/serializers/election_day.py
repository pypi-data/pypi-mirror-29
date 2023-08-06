from election.models import ElectionDay
from rest_framework import serializers


class ElectionDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionDay
        fields = '__all__'
