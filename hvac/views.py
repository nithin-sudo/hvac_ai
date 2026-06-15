from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from hvac.models import HVACHealthAssessment, HVACTripSummary, Vehicle
from hvac.serializers import (
    HVACHealthAssessmentSerializer,
    HVACTripSummarySerializer,
    VehicleSerializer,
)


class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all().order_by('vin')
    serializer_class = VehicleSerializer
    lookup_field = 'vin'


class HVACTripSummaryViewSet(viewsets.ModelViewSet):
    queryset = HVACTripSummary.objects.select_related('vehicle', 'assessment').all()
    serializer_class = HVACTripSummarySerializer


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


@api_view(['GET'])
def dealer_report(request, vin: str):
    assessment = (
        HVACHealthAssessment.objects.select_related('vehicle', 'trip')
        .filter(vehicle__vin=vin)
        .first()
    )
    if assessment is None:
        return Response(
            {'detail': 'No dealer report found for this vehicle.'},
            status=status.HTTP_404_NOT_FOUND,
        )

    return Response(
        {
            'vin': assessment.vehicle.vin,
            'risk_level': assessment.risk_level,
            'confidence': assessment.confidence,
            'likely_issue': assessment.likely_issue,
            'recommended_action': assessment.recommended_action,
            'dealer_summary': assessment.dealer_summary,
        }
    )


@api_view(['GET'])
def fleet_hvac_risk(request):
    risk_counts = (
        HVACHealthAssessment.objects.values('risk_level')
        .annotate(count=Count('id'))
        .order_by('risk_level')
    )
    latest_high_risk = (
        HVACHealthAssessment.objects.select_related('vehicle', 'trip')
        .filter(risk_level='high')[:10]
    )
    return Response(
        {
            'risk_counts': list(risk_counts),
            'latest_high_risk': HVACHealthAssessmentSerializer(
                latest_high_risk,
                many=True,
            ).data,
        }
    )
