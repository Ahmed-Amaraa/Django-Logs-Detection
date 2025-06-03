from django.conf import settings
from transformers import pipeline
from django.core.mail import send_mail
from django.template.loader import render_to_string

class NotificationManager:
    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def generate_summary(self, log_entry, anomaly_report):
        # Combine log context for summarization
        context = f"Log Message: {log_entry.message}\n"
        context += f"Severity: {log_entry.severity}\n"
        context += f"Source: {log_entry.source}\n"
        context += f"Anomaly Score: {anomaly_report.anomaly_score}"

        # Generate AI summary
        summary = self.summarizer(context, max_length=50, min_length=10)[0]['summary_text']
        return summary

    def send_notification(self, anomaly_report):
        # Temporarily skip email notification
        pass
        summary = self.generate_summary(anomaly_report.log_entry, anomaly_report)
        
        # Email notification
        subject = f'Anomaly Detected - Score: {anomaly_report.anomaly_score:.2f}'
        message = render_to_string('model/email/anomaly_notification.html', {
            'anomaly': anomaly_report,
            'summary': summary,
        })

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=settings.NOTIFICATION_RECIPIENTS,
            html_message=message
        )

# Initialize notification manager
notifier = NotificationManager()