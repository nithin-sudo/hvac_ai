from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hvac.models import HVACHealthAssessment, Vehicle
from hvac.serializers import HVACHealthAssessmentSerializer, VehicleSerializer


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('vin')
    serializer_class = VehicleSerializer
    lookup_field = 'vin'


@api_view(['GET'])
def vehicle_health(request, vin: str):
    assessment = (
        HVACHealthAssessment.objects.select_related('vehicle', 'trip')
        .filter(vehicle__vin=vin)
        .first()
    )
    if assessment is None:
        return Response(
            {'detail': 'No HVAC health assessment found for this vehicle.'},
            status=status.HTTP_404_NOT_FOUND,
        )
    return Response(HVACHealthAssessmentSerializer(assessment).data)
