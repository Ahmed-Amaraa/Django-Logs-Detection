from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime

def validate_timestamp_order(value):
    from django.utils import timezone
    if value > timezone.now():
        raise ValidationError('Timestamp cannot be in the future')

class LogEntry(models.Model):
    SEVERITY_CHOICES = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical')
    ]

    timestamp = models.DateTimeField(validators=[validate_timestamp_order])
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    message = models.TextField()
    source = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['severity']),
        ]

    def __str__(self):
        return f"{self.timestamp} - {self.severity}: {self.message[:50]}"

class AnomalyReport(models.Model):
    log_entry = models.ForeignKey(LogEntry, on_delete=models.CASCADE, related_name='anomalies')
    anomaly_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)]
    )
    detection_timestamp = models.DateTimeField(auto_now_add=True)
    model_version = models.CharField(max_length=50)
    summary = models.TextField()
    is_acknowledged = models.BooleanField(default=False)

    class Meta:
        ordering = ['-detection_timestamp']
        indexes = [
            models.Index(fields=['anomaly_score']),
            models.Index(fields=['detection_timestamp']),
        ]

    def __str__(self):
        return f"Anomaly {self.anomaly_score:.2f} - {self.log_entry}"
