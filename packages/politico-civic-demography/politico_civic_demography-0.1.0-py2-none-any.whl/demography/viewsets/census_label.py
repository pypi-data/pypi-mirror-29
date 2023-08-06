from demography.models import CensusLabel
from demography.serializers import CensusLabelSerializer

from .base import BaseViewSet


class CensusLabelViewSet(BaseViewSet):
    queryset = CensusLabel.objects.all()
    serializer_class = CensusLabelSerializer
