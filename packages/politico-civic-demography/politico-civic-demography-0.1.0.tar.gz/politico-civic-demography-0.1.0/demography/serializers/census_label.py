from demography.models import CensusLabel
from rest_framework import serializers


class CensusLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CensusLabel
        fields = '__all__'
