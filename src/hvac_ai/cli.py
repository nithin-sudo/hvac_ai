from __future__ import annotations

from hvac_ai.sample_data import SAMPLE_TRIPS
from hvac_ai.scoring import assess_trip


def main() -> None:
    print("HVAC Predictive Health - Day 1 Demo")
    print("=" * 42)

    for trip in SAMPLE_TRIPS:
        assessment = assess_trip(trip)
        print(f"\nVehicle: {assessment.vehicle_id}")
        print(f"Health score: {assessment.health_score}")
        print(f"Risk level: {assessment.risk_level.value}")
        print(f"Likely issue: {assessment.likely_issue}")
        print(f"Confidence: {assessment.confidence:.2f}")
        print(f"Action: {assessment.recommended_action}")
        print(f"Customer: {assessment.customer_message}")
        print(f"Dealer: {assessment.dealer_summary}")


if __name__ == "__main__":
    main()
