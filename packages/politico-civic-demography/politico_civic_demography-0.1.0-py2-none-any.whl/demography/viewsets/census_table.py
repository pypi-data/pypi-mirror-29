from demography.models import CensusTable
from demography.serializers import CensusTableSerializer

from .base import BaseViewSet


class CensusTableViewSet(BaseViewSet):
    queryset = CensusTable.objects.all()
    serializer_class = CensusTableSerializer
