from demography.models import CensusEstimate
from demography.serializers import CensusEstimateSerializer

from .base import BaseViewSet


class CensusEstimateViewSet(BaseViewSet):
    queryset = CensusEstimate.objects.all()
    serializer_class = CensusEstimateSerializer
