from rest_framework import viewsets

from hvac.models import NotificationEvent
from hvac.serializers import NotificationEventSerializer


class NotificationEventViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = NotificationEventSerializer

    def get_queryset(self):
        queryset = NotificationEvent.objects.select_related(
            'assessment',
            'assessment__vehicle',
        )
        vin = self.request.query_params.get('vin')
        audience = self.request.query_params.get('audience')
        pending = self.request.query_params.get('pending')

        if vin:
            queryset = queryset.filter(assessment__vehicle__vin=vin)
        if audience:
            queryset = queryset.filter(audience=audience)
        if pending in {'1', 'true', 'yes'}:
            queryset = queryset.filter(should_send=True, sent_at__isnull=True)

        return queryset
