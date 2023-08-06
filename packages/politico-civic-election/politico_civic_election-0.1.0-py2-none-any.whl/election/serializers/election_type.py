from election.models import ElectionType
from rest_framework import serializers


class ElectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElectionType
        fields = '__all__'
