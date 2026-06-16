from rest_framework import serializers

from hvac.models import HVACHealthAssessment, HVACTripSummary, NotificationEvent, Vehicle
from hvac.scoring import assess_trip


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            'id',
            'vin',
            'model',
            'model_year',
            'region',
            'hvac_software_version',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class HVACHealthAssessmentSerializer(serializers.ModelSerializer):
    vin = serializers.CharField(source='vehicle.vin', read_only=True)
    trip_id = serializers.IntegerField(source='trip.id', read_only=True)

    class Meta:
        model = HVACHealthAssessment
        fields = [
            'id',
            'trip_id',
            'vin',
            'health_score',
            'risk_level',
            'likely_issue',
            'confidence',
            'recommended_action',
            'customer_message',
            'dealer_summary',
            'created_at',
        ]
        read_only_fields = fields


class HVACTripSummarySerializer(serializers.ModelSerializer):
    vin = serializers.SlugRelatedField(
        source='vehicle',
        slug_field='vin',
        queryset=Vehicle.objects.all(),
        write_only=True,
    )
    vehicle_vin = serializers.CharField(source='vehicle.vin', read_only=True)
    assessment = HVACHealthAssessmentSerializer(read_only=True)

    class Meta:
        model = HVACTripSummary
        fields = [
            'id',
            'vin',
            'vehicle_vin',
            'observed_at',
            'ambient_temp_f',
            'cabin_start_temp_f',
            'target_temp_f',
            'vent_temp_min_f',
            'time_to_target_min',
            'compressor_duty_avg',
            'pressure_stability',
            'fault_code_count',
            'assessment',
            'created_at',
        ]
        read_only_fields = ['id', 'vehicle_vin', 'assessment', 'created_at']

    def create(self, validated_data):
        trip = super().create(validated_data)
        result = assess_trip(trip)
        HVACHealthAssessment.objects.create(
            trip=trip,
            vehicle=trip.vehicle,
            health_score=result.health_score,
            risk_level=result.risk_level,
            likely_issue=result.likely_issue,
            confidence=result.confidence,
            recommended_action=result.recommended_action,
            customer_message=result.customer_message,
            dealer_summary=result.dealer_summary,
        )
        return trip


class NotificationEventSerializer(serializers.ModelSerializer):
    assessment_id = serializers.IntegerField(source='assessment.id', read_only=True)
    vin = serializers.CharField(source='assessment.vehicle.vin', read_only=True)

    class Meta:
        model = NotificationEvent
        fields = [
            'id',
            'assessment_id',
            'vin',
            'audience',
            'message',
            'should_send',
            'sent_at',
            'created_at',
        ]
        read_only_fields = ['id', 'assessment_id', 'vin', 'created_at']
