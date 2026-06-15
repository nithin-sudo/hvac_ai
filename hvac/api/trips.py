from rest_framework import viewsets

from hvac.models import HVACTripSummary
from hvac.serializers import HVACTripSummarySerializer


class HVACTripSummaryViewSet(viewsets.ModelViewSet):
    queryset = HVACTripSummary.objects.select_related('vehicle', 'assessment').all()
    serializer_class = HVACTripSummarySerializer
