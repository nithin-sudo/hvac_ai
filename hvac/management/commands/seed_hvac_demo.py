from django.core.management.base import BaseCommand
from django.utils import timezone

from hvac.models import HVACTripSummary, Vehicle
from hvac.services.assessments import create_assessment_for_trip


class Command(BaseCommand):
    help = 'Seed demo HVAC vehicles, trip summaries, assessments, and notifications.'

    def handle(self, *args, **options):
        demo_rows = [
            {
                'vehicle': {
                    'vin': 'VIN-HVAC-001',
                    'model': 'Pilot',
                    'model_year': 2026,
                    'region': 'TX',
                    'hvac_software_version': 'hvac-1.2.3',
                },
                'trip': {
                    'ambient_temp_f': 94,
                    'cabin_start_temp_f': 104,
                    'target_temp_f': 72,
                    'vent_temp_min_f': 51,
                    'time_to_target_min': 17,
                    'compressor_duty_avg': 0.88,
                    'pressure_stability': 0.72,
                    'fault_code_count': 0,
                },
            },
            {
                'vehicle': {
                    'vin': 'VIN-HVAC-002',
                    'model': 'Accord',
                    'model_year': 2026,
                    'region': 'MI',
                    'hvac_software_version': 'hvac-1.2.3',
                },
                'trip': {
                    'ambient_temp_f': 78,
                    'cabin_start_temp_f': 88,
                    'target_temp_f': 72,
                    'vent_temp_min_f': 43,
                    'time_to_target_min': 7,
                    'compressor_duty_avg': 0.42,
                    'pressure_stability': 0.91,
                    'fault_code_count': 0,
                },
            },
            {
                'vehicle': {
                    'vin': 'VIN-HVAC-003',
                    'model': 'CR-V',
                    'model_year': 2025,
                    'region': 'AZ',
                    'hvac_software_version': 'hvac-1.2.2',
                },
                'trip': {
                    'ambient_temp_f': 101,
                    'cabin_start_temp_f': 116,
                    'target_temp_f': 72,
                    'vent_temp_min_f': 58,
                    'time_to_target_min': 24,
                    'compressor_duty_avg': 0.96,
                    'pressure_stability': 0.48,
                    'fault_code_count': 2,
                },
            },
        ]

        for row in demo_rows:
            vehicle, _ = Vehicle.objects.update_or_create(
                vin=row['vehicle']['vin'],
                defaults=row['vehicle'],
            )
            trip = HVACTripSummary.objects.create(
                vehicle=vehicle,
                observed_at=timezone.now(),
                **row['trip'],
            )
            assessment = create_assessment_for_trip(trip)
            self.stdout.write(
                self.style.SUCCESS(
                    f'{vehicle.vin}: {assessment.risk_level} risk, '
                    f'score={assessment.health_score}'
                )
            )
