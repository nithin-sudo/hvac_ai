from __future__ import annotations

from django.db import transaction

from hvac.models import HVACHealthAssessment, HVACTripSummary, NotificationEvent
from hvac.scoring import assess_trip
from hvac.services.notifications import create_notification_events


@transaction.atomic
def create_assessment_for_trip(trip: HVACTripSummary) -> HVACHealthAssessment:
    result = assess_trip(trip)
    assessment = HVACHealthAssessment.objects.create(
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
    create_notification_events(assessment)
    return assessment


def latest_assessment_for_vehicle(vin: str) -> HVACHealthAssessment | None:
    return (
        HVACHealthAssessment.objects.select_related('vehicle', 'trip')
        .prefetch_related('notifications')
        .filter(vehicle__vin=vin)
        .first()
    )


def pending_notifications_for_vehicle(vin: str):
    return NotificationEvent.objects.select_related(
        'assessment',
        'assessment__vehicle',
    ).filter(
        assessment__vehicle__vin=vin,
        should_send=True,
        sent_at__isnull=True,
    )
