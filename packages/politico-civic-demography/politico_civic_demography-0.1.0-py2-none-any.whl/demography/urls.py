from django.urls import include, path
from rest_framework import routers

from .viewsets import (CensusEstimateViewSet, CensusLabelViewSet,
                       CensusTableViewSet, CensusVariableViewSet)

router = routers.DefaultRouter()

router.register(r'census-tables', CensusTableViewSet)
router.register(r'census-labels', CensusLabelViewSet)
router.register(r'census-variables', CensusVariableViewSet)
router.register(r'census-estimates', CensusEstimateViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
