from __future__ import annotations

from hvac.models import HVACHealthAssessment, NotificationEvent


def create_notification_events(assessment: HVACHealthAssessment) -> list[NotificationEvent]:
    events: list[NotificationEvent] = []

    if assessment.risk_level in {'medium', 'high'}:
        events.append(
            NotificationEvent(
                assessment=assessment,
                audience=NotificationEvent.Audience.CUSTOMER,
                message=assessment.customer_message,
                should_send=True,
            )
        )
        events.append(
            NotificationEvent(
                assessment=assessment,
                audience=NotificationEvent.Audience.DEALER,
                message=assessment.dealer_summary,
                should_send=True,
            )
        )

    events.append(
        NotificationEvent(
            assessment=assessment,
            audience=NotificationEvent.Audience.OEM,
            message=_oem_message(assessment),
            should_send=assessment.risk_level != 'low',
        )
    )

    return NotificationEvent.objects.bulk_create(events)


def _oem_message(assessment: HVACHealthAssessment) -> str:
    return (
        f'{assessment.vehicle.vin} HVAC risk={assessment.risk_level}, '
        f'issue={assessment.likely_issue}, score={assessment.health_score}, '
        f'confidence={assessment.confidence:.2f}.'
    )
