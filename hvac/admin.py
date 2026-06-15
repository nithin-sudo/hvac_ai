from django.contrib import admin

from hvac.models import HVACHealthAssessment, HVACTripSummary, NotificationEvent, Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vin', 'model', 'model_year', 'region', 'hvac_software_version')
    search_fields = ('vin', 'model', 'region', 'hvac_software_version')


@admin.register(HVACTripSummary)
class HVACTripSummaryAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'observed_at', 'time_to_target_min', 'vent_temp_min_f')
    list_filter = ('vehicle__region', 'vehicle__hvac_software_version')
    search_fields = ('vehicle__vin',)


@admin.register(HVACHealthAssessment)
class HVACHealthAssessmentAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'risk_level', 'health_score', 'likely_issue', 'created_at')
    list_filter = ('risk_level', 'likely_issue')
    search_fields = ('vehicle__vin', 'likely_issue')


@admin.register(NotificationEvent)
class NotificationEventAdmin(admin.ModelAdmin):
    list_display = ('assessment', 'audience', 'should_send', 'sent_at', 'created_at')
    list_filter = ('audience', 'should_send')
