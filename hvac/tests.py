from django.test import TestCase
from django.utils import timezone

from hvac.models import HVACTripSummary, NotificationEvent, Vehicle
from hvac.services.assessments import create_assessment_for_trip


class AssessmentWorkflowTests(TestCase):
    def test_medium_risk_trip_creates_customer_dealer_and_oem_notifications(self):
        vehicle = Vehicle.objects.create(
            vin='VIN-HVAC-101',
            model='Pilot',
            model_year=2026,
            region='TX',
            hvac_software_version='hvac-1.2.3',
        )
        trip = HVACTripSummary.objects.create(
            vehicle=vehicle,
            observed_at=timezone.now(),
            ambient_temp_f=94,
            cabin_start_temp_f=104,
            target_temp_f=72,
            vent_temp_min_f=51,
            time_to_target_min=17,
            compressor_duty_avg=0.88,
            pressure_stability=0.72,
            fault_code_count=0,
        )

        assessment = create_assessment_for_trip(trip)

        self.assertEqual(assessment.risk_level, 'medium')
        self.assertEqual(assessment.notifications.count(), 3)
        self.assertEqual(
            set(assessment.notifications.values_list('audience', flat=True)),
            {'customer', 'dealer', 'oem'},
        )

    def test_low_risk_trip_creates_oem_record_but_no_sendable_customer_alert(self):
        vehicle = Vehicle.objects.create(
            vin='VIN-HVAC-102',
            model='Pilot',
            model_year=2026,
            region='MI',
            hvac_software_version='hvac-1.2.3',
        )
        trip = HVACTripSummary.objects.create(
            vehicle=vehicle,
            observed_at=timezone.now(),
            ambient_temp_f=78,
            cabin_start_temp_f=88,
            target_temp_f=72,
            vent_temp_min_f=43,
            time_to_target_min=7,
            compressor_duty_avg=0.42,
            pressure_stability=0.91,
            fault_code_count=0,
        )

        assessment = create_assessment_for_trip(trip)

        self.assertEqual(assessment.risk_level, 'low')
        self.assertEqual(assessment.notifications.count(), 1)
        notification = assessment.notifications.get()
        self.assertEqual(notification.audience, NotificationEvent.Audience.OEM)
        self.assertFalse(notification.should_send)
