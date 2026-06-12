from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass(frozen=True)
class HVACTripSummary:
    vehicle_id: str
    timestamp: datetime
    region: str
    ambient_temp_f: float
    cabin_start_temp_f: float
    target_temp_f: float
    vent_temp_min_f: float
    time_to_target_min: float
    compressor_duty_avg: float
    pressure_stability: float
    fault_code_count: int
    software_version: str


@dataclass(frozen=True)
class HVACHealthAssessment:
    vehicle_id: str
    health_score: int
    risk_level: RiskLevel
    likely_issue: str
    confidence: float
    recommended_action: str
    customer_message: str
    dealer_summary: str
