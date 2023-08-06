from demography.models import CensusVariable
from demography.serializers import CensusVariableSerializer

from .base import BaseViewSet


class CensusVariableViewSet(BaseViewSet):
    queryset = CensusVariable.objects.all()
    serializer_class = CensusVariableSerializer
