import unittest

from hvac_ai.sample_data import SAMPLE_TRIPS
from hvac_ai.scoring import assess_trip


class HVACScoringTest(unittest.TestCase):
    def test_high_risk_trip_scores_below_healthy_trip(self) -> None:
        high_risk = assess_trip(SAMPLE_TRIPS[2])
        healthy = assess_trip(SAMPLE_TRIPS[1])

        self.assertLess(high_risk.health_score, healthy.health_score)
        self.assertEqual(high_risk.risk_level.value, "high")
        self.assertEqual(healthy.risk_level.value, "low")

    def test_medium_trip_creates_customer_guidance(self) -> None:
        assessment = assess_trip(SAMPLE_TRIPS[0])

        self.assertEqual(assessment.risk_level.value, "medium")
        self.assertEqual(assessment.recommended_action, "schedule_inspection_14_days")
        self.assertIn("AC is taking longer", assessment.customer_message)


if __name__ == "__main__":
    unittest.main()
