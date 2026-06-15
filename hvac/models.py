from django.db import models


class Vehicle(models.Model):
    vin = models.CharField(max_length=32, unique=True)
    model = models.CharField(max_length=80)
    model_year = models.PositiveSmallIntegerField()
    region = models.CharField(max_length=40)
    hvac_software_version = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vin


class HVACTripSummary(models.Model):
    vehicle = models.ForeignKey(
        Vehicle,
        related_name='hvac_trips',
        on_delete=models.CASCADE,
    )
    observed_at = models.DateTimeField()
    ambient_temp_f = models.FloatField()
    cabin_start_temp_f = models.FloatField()
    target_temp_f = models.FloatField()
    vent_temp_min_f = models.FloatField()
    time_to_target_min = models.FloatField()
    compressor_duty_avg = models.FloatField()
    pressure_stability = models.FloatField()
    fault_code_count = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-observed_at']

    def __str__(self) -> str:
        return f'{self.vehicle.vin} at {self.observed_at.isoformat()}'


class HVACHealthAssessment(models.Model):
    class RiskLevel(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'

    trip = models.OneToOneField(
        HVACTripSummary,
        related_name='assessment',
        on_delete=models.CASCADE,
    )
    vehicle = models.ForeignKey(
        Vehicle,
        related_name='hvac_assessments',
        on_delete=models.CASCADE,
    )
    health_score = models.PositiveSmallIntegerField()
    risk_level = models.CharField(max_length=16, choices=RiskLevel.choices)
    likely_issue = models.CharField(max_length=80)
    confidence = models.FloatField()
    recommended_action = models.CharField(max_length=80)
    customer_message = models.TextField()
    dealer_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.vehicle.vin}: {self.risk_level} ({self.health_score})'


class NotificationEvent(models.Model):
    class Audience(models.TextChoices):
        CUSTOMER = 'customer', 'Customer'
        DEALER = 'dealer', 'Dealer'
        OEM = 'oem', 'OEM'

    assessment = models.ForeignKey(
        HVACHealthAssessment,
        related_name='notifications',
        on_delete=models.CASCADE,
    )
    audience = models.CharField(max_length=16, choices=Audience.choices)
    message = models.TextField()
    should_send = models.BooleanField(default=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f'{self.audience}: {self.assessment.vehicle.vin}'
