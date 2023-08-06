from demography.models import CensusEstimate
from rest_framework import serializers


class CensusEstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CensusEstimate
        fields = '__all__'
