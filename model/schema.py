import graphene
from graphene_django import DjangoObjectType
from .models import LogEntry, AnomalyReport

class LogEntryType(DjangoObjectType):
    class Meta:
        model = LogEntry
        fields = ('id', 'timestamp', 'severity', 'message', 'source', 'metadata', 'created_at')

class AnomalyReportType(DjangoObjectType):
    class Meta:
        model = AnomalyReport
        fields = ('id', 'log_entry', 'anomaly_score', 'detection_timestamp', 'model_version', 'summary', 'is_acknowledged')

class Query(graphene.ObjectType):
    all_logs = graphene.List(
        LogEntryType,
        severity=graphene.String(),
        source=graphene.String(),
        min_timestamp=graphene.DateTime(),
    )
    all_anomalies = graphene.List(
        AnomalyReportType,
        min_score=graphene.Float(),
        is_acknowledged=graphene.Boolean(),
    )
    log_entry = graphene.Field(LogEntryType, id=graphene.ID(required=True))
    anomaly_report = graphene.Field(AnomalyReportType, id=graphene.ID(required=True))

    def resolve_all_logs(self, info, severity=None, source=None, min_timestamp=None):
        queryset = LogEntry.objects.all()
        if severity:
            queryset = queryset.filter(severity=severity)
        if source:
            queryset = queryset.filter(source=source)
        if min_timestamp:
            queryset = queryset.filter(timestamp__gte=min_timestamp)
        return queryset

    def resolve_all_anomalies(self, info, min_score=None, is_acknowledged=None):
        queryset = AnomalyReport.objects.all()
        if min_score is not None:
            queryset = queryset.filter(anomaly_score__gte=min_score)
        if is_acknowledged is not None:
            queryset = queryset.filter(is_acknowledged=is_acknowledged)
        return queryset

    def resolve_log_entry(self, info, id):
        return LogEntry.objects.get(pk=id)

    def resolve_anomaly_report(self, info, id):
        return AnomalyReport.objects.get(pk=id)

class AcknowledgeAnomaly(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    anomaly = graphene.Field(AnomalyReportType)

    def mutate(self, info, id):
        anomaly = AnomalyReport.objects.get(pk=id)
        anomaly.is_acknowledged = True
        anomaly.save()
        return AcknowledgeAnomaly(anomaly=anomaly)

class CreateLogEntry(graphene.Mutation):
    class Arguments:
        timestamp = graphene.String(required=True)
        severity = graphene.String(required=True)
        message = graphene.String(required=True)
        source = graphene.String(required=True)
        metadata = graphene.JSONString(required=False)

    log_entry = graphene.Field(LogEntryType)

    def mutate(self, info, timestamp, severity, message, source, metadata=None):
        from datetime import datetime
        try:
            # Convert timestamp string to datetime
            dt = datetime.strptime(timestamp, "%d/%m/%Y %H:%M")
            
            # Validate severity
            if severity not in dict(LogEntry.SEVERITY_CHOICES):
                raise ValueError(f"Invalid severity. Must be one of {dict(LogEntry.SEVERITY_CHOICES).keys()}")
            
            # Create log entry
            log_entry = LogEntry.objects.create(
                timestamp=dt,
                severity=severity,
                message=message,
                source=source,
                metadata=metadata or {}
            )
            
            return CreateLogEntry(log_entry=log_entry)
            
        except ValueError as e:
            raise graphene.GraphQLError(str(e))

class Mutation(graphene.ObjectType):
    acknowledge_anomaly = AcknowledgeAnomaly.Field()
    create_log_entry = CreateLogEntry.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)