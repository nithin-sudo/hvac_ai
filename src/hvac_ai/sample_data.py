from __future__ import annotations

from datetime import datetime, timezone

from hvac_ai.models import HVACTripSummary


SAMPLE_TRIPS: tuple[HVACTripSummary, ...] = (
    HVACTripSummary(
        vehicle_id="VIN-HVAC-001",
        timestamp=datetime(2026, 6, 12, 9, 30, tzinfo=timezone.utc),
        region="TX",
        ambient_temp_f=94,
        cabin_start_temp_f=104,
        target_temp_f=72,
        vent_temp_min_f=51,
        time_to_target_min=17,
        compressor_duty_avg=0.88,
        pressure_stability=0.72,
        fault_code_count=0,
        software_version="hvac-1.2.3",
    ),
    HVACTripSummary(
        vehicle_id="VIN-HVAC-002",
        timestamp=datetime(2026, 6, 12, 10, 15, tzinfo=timezone.utc),
        region="MI",
        ambient_temp_f=78,
        cabin_start_temp_f=88,
        target_temp_f=72,
        vent_temp_min_f=43,
        time_to_target_min=7,
        compressor_duty_avg=0.42,
        pressure_stability=0.91,
        fault_code_count=0,
        software_version="hvac-1.2.3",
    ),
    HVACTripSummary(
        vehicle_id="VIN-HVAC-003",
        timestamp=datetime(2026, 6, 12, 11, 45, tzinfo=timezone.utc),
        region="AZ",
        ambient_temp_f=101,
        cabin_start_temp_f=116,
        target_temp_f=72,
        vent_temp_min_f=58,
        time_to_target_min=24,
        compressor_duty_avg=0.96,
        pressure_stability=0.48,
        fault_code_count=2,
        software_version="hvac-1.2.2",
    ),
)
