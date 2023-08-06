from demography.models import CensusTable
from rest_framework import serializers


class CensusTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CensusTable
        fields = '__all__'
