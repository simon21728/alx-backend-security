from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ip_tracking.models import SuspiciousIP
from django.db.models import Count
from django.conf import settings
from myapp.models import RequestLog  # Replace with your actual model logging requests

@shared_task
def detect_suspicious_ips():
    """
    Task to detect IPs exceeding 100 requests/hour or accessing sensitive paths.
    """
    one_hour_ago = timezone.now() - timedelta(hours=1)

    # Detect IPs exceeding 100 requests/hour
    frequent_ips = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago)
        .values('ip_address')
        .annotate(request_count=Count('id'))
        .filter(request_count__gt=100)
    )

    for entry in frequent_ips:
        SuspiciousIP.objects.update_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': f'Exceeded 100 requests in the last hour ({entry["request_count"]})'}
        )

    # Detect IPs accessing sensitive paths
    sensitive_paths = ['/admin', '/login']
    sensitive_ips = (
        RequestLog.objects.filter(timestamp__gte=one_hour_ago, path__in=sensitive_paths)
        .values('ip_address')
        .distinct()
    )

    for entry in sensitive_ips:
        SuspiciousIP.objects.update_or_create(
            ip_address=entry['ip_address'],
            defaults={'reason': 'Accessed sensitive path'}
        )
