from django.shortcuts import render
from rest_framework.decorators import action
from .serializers import LogEntrySerializer, AnomalyReportSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from .models import LogEntry, AnomalyReport
from .ml_utils import LogAnomalyDetector
#from .notifications import notifier
from django.shortcuts import redirect

# Initialize the detector
detector = LogAnomalyDetector()

class LogEntryViewSet(viewsets.ModelViewSet):
    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['severity', 'source']
    ordering_fields = ['timestamp', 'created_at']
    ordering = ['-timestamp']

    def perform_create(self, serializer):
        log_entry = serializer.save()
        
        # Analyze log with BERT
        analysis = detector.analyze_log(log_entry.message)
        
        if analysis['is_anomaly']:
            # Create anomaly report
            anomaly_report = AnomalyReport.objects.create(
                log_entry=log_entry,
                anomaly_score=analysis['anomaly_score'],
                model_version=analysis['model_version'],
                summary=f'BERT detected anomaly in log message'
            )
        else:
            anomaly_report = AnomalyReport.objects.create(
                log_entry=log_entry,
                anomaly_score=analysis['anomaly_score'],
                model_version=analysis['model_version'],
                summary=f'No anomaly detected!!'
            )
            # Send notification
            #notifier.send_notification(anomaly_report)
            
            # Return redirect response
            return redirect('/api/anomalies/')

class AnomalyReportViewSet(viewsets.ModelViewSet):
    queryset = AnomalyReport.objects.all()
    serializer_class = AnomalyReportSerializer
    # permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_acknowledged', 'model_version']
    ordering_fields = ['anomaly_score', 'detection_timestamp']
    ordering = ['-detection_timestamp']

    @action(detail=True, methods=['post'])
    def acknowledge(self, request, pk=None):
        anomaly = self.get_object()
        anomaly.is_acknowledged = True
        anomaly.save()
        return Response({'status': 'anomaly acknowledged'}, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()
        min_score = self.request.query_params.get('min_score', None)
        if min_score is not None:
            queryset = queryset.filter(anomaly_score__gte=float(min_score))
        return queryset

