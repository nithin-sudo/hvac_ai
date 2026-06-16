from django.urls import path
from rest_framework.routers import DefaultRouter

from hvac.api.notifications import NotificationEventViewSet
from hvac.api.reports import dealer_report, fleet_hvac_risk
from hvac.api.trips import HVACTripSummaryViewSet
from hvac.api.vehicles import VehicleViewSet, vehicle_health

router = DefaultRouter()
router.register('vehicles', VehicleViewSet, basename='vehicle')
router.register('hvac/trips', HVACTripSummaryViewSet, basename='hvac-trip')
router.register('notifications', NotificationEventViewSet, basename='notification')

urlpatterns = [
    path('vehicles/<str:vin>/health/', vehicle_health, name='vehicle-health'),
    path('vehicles/<str:vin>/dealer-report/', dealer_report, name='dealer-report'),
    path('fleet/hvac-risk/', fleet_hvac_risk, name='fleet-hvac-risk'),
]

urlpatterns += router.urls
