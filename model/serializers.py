from rest_framework import serializers
from .models import LogEntry, AnomalyReport
from datetime import datetime

class LogEntrySerializer(serializers.ModelSerializer):
    # Add a custom field for timestamp input
    timestamp = serializers.CharField(write_only=True)
    formatted_timestamp = serializers.DateTimeField(source='timestamp', read_only=True)

    class Meta:
        model = LogEntry
        fields = ['id', 'timestamp', 'formatted_timestamp', 'severity', 'message', 'source', 'metadata', 'created_at']
        read_only_fields = ['created_at']

    def validate_timestamp(self, value):
        try:
            # Convert the input string to datetime
            dt = datetime.strptime(value, "%d/%m/%Y %H:%M")
            return dt
        except ValueError:
            raise serializers.ValidationError(
                "Invalid timestamp format. Use DD/MM/YYYY HH:MM format (e.g., 20/02/2025 21:30)"
            )

    def validate_severity(self, value):
        if value not in dict(LogEntry.SEVERITY_CHOICES):
            raise serializers.ValidationError(f"Invalid severity level. Choose from {dict(LogEntry.SEVERITY_CHOICES).keys()}")
        return value

class AnomalyReportSerializer(serializers.ModelSerializer):
    log_entry = LogEntrySerializer(read_only=True)

    class Meta:
        model = AnomalyReport
        fields = ['id', 'log_entry', 'anomaly_score', 'detection_timestamp', 'model_version', 'summary', 'is_acknowledged']
        read_only_fields = ['detection_timestamp']