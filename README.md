# Django Logs Detection
A sophisticated log management and anomaly detection system built with Django and GraphQL. This system helps monitor, analyze, and detect anomalies in application logs in real-time.

**Log Management**
  - Create and store log entries with timestamp, severity, message, and source

**Anomaly Detection**
  - Automated anomaly detection on log entries
  - Configurable anomaly scoring system
  - Real-time anomaly reporting
 **GraphQL API**
  - Supports complex queries and mutations
  - Built with Graphene-Django


### GraphQL Queries
- allLogs: Retrieve log entries with optional filtering
- allAnomalies: Get anomaly reports with score filtering
- logEntry: Get a specific log entry by ID
- anomalyReport: Get a specific anomaly report by ID

### GraphQL Mutations
- createLogEntry: Create a new log entry
- acknowledgeAnomaly: Mark an anomaly as acknowledged



