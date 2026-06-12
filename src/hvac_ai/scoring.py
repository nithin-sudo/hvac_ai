from __future__ import annotations

from hvac_ai.models import HVACHealthAssessment, HVACTripSummary, RiskLevel


def assess_trip(trip: HVACTripSummary) -> HVACHealthAssessment:
    """Score a single HVAC trip summary with transparent Day 1 rules."""
    risk_points = 0
    reasons: list[str] = []

    if trip.time_to_target_min >= 20:
        risk_points += 30
        reasons.append("very slow cabin cooling")
    elif trip.time_to_target_min >= 14:
        risk_points += 18
        reasons.append("slower than expected cabin cooling")

    if trip.compressor_duty_avg >= 0.9:
        risk_points += 24
        reasons.append("high compressor effort")
    elif trip.compressor_duty_avg >= 0.8:
        risk_points += 14
        reasons.append("elevated compressor effort")

    if trip.vent_temp_min_f >= 56:
        risk_points += 22
        reasons.append("weak vent temperature drop")
    elif trip.vent_temp_min_f >= 50:
        risk_points += 12
        reasons.append("borderline vent temperature")

    if trip.pressure_stability <= 0.55:
        risk_points += 18
        reasons.append("unstable refrigerant pressure behavior")
    elif trip.pressure_stability <= 0.7:
        risk_points += 10
        reasons.append("reduced pressure stability")

    if trip.fault_code_count > 0:
        risk_points += min(16, trip.fault_code_count * 8)
        reasons.append("recent HVAC fault code activity")

    health_score = max(0, 100 - risk_points)
    risk_level = _risk_level(health_score)
    likely_issue = _likely_issue(reasons)
    confidence = _confidence(risk_points, len(reasons))

    return HVACHealthAssessment(
        vehicle_id=trip.vehicle_id,
        health_score=health_score,
        risk_level=risk_level,
        likely_issue=likely_issue,
        confidence=confidence,
        recommended_action=_recommended_action(risk_level),
        customer_message=_customer_message(risk_level),
        dealer_summary=_dealer_summary(trip, reasons),
    )


def _risk_level(health_score: int) -> RiskLevel:
    if health_score < 50:
        return RiskLevel.HIGH
    if health_score < 75:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def _likely_issue(reasons: list[str]) -> str:
    if not reasons:
        return "no_current_hvac_degradation_signal"
    if "weak vent temperature drop" in reasons or "borderline vent temperature" in reasons:
        return "cooling_efficiency_degradation"
    if "unstable refrigerant pressure behavior" in reasons:
        return "pressure_stability_degradation"
    if "high compressor effort" in reasons or "elevated compressor effort" in reasons:
        return "compressor_effort_degradation"
    return "hvac_performance_drift"


def _confidence(risk_points: int, reason_count: int) -> float:
    base = min(0.9, 0.45 + (risk_points / 100))
    reason_bonus = min(0.08, reason_count * 0.02)
    return round(min(0.95, base + reason_bonus), 2)


def _recommended_action(risk_level: RiskLevel) -> str:
    if risk_level is RiskLevel.HIGH:
        return "schedule_inspection_7_days"
    if risk_level is RiskLevel.MEDIUM:
        return "schedule_inspection_14_days"
    return "continue_monitoring"


def _customer_message(risk_level: RiskLevel) -> str:
    if risk_level is RiskLevel.HIGH:
        return "Your AC may need attention soon. Schedule service within 7 days."
    if risk_level is RiskLevel.MEDIUM:
        return "Your AC is taking longer than normal to cool the cabin. Schedule inspection within 14 days."
    return "Your climate system looks normal based on recent trips."


def _dealer_summary(trip: HVACTripSummary, reasons: list[str]) -> str:
    if not reasons:
        reason_text = "No abnormal HVAC pattern detected."
    else:
        reason_text = "; ".join(reasons)

    return (
        f"{trip.vehicle_id}: {reason_text} "
        f"(software={trip.software_version}, region={trip.region}, "
        f"time_to_target={trip.time_to_target_min}min, "
        f"compressor_duty={trip.compressor_duty_avg:.2f}, "
        f"pressure_stability={trip.pressure_stability:.2f})."
    )
