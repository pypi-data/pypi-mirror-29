from demography.models import CensusVariable
from rest_framework import serializers


class CensusVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = CensusVariable
        fields = '__all__'
