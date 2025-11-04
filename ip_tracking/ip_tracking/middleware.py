# ip_tracking/middleware.py

from .models import RequestLog

class IPLoggingMiddleware:
    """
    Middleware that logs the IP address, timestamp, and path
    of every incoming request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extract IP address
        ip_address = self.get_client_ip(request)
        path = request.path

        # Log the request
        RequestLog.objects.create(ip_address=ip_address, path=path)

        # Continue processing
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        """Try to get the real IP address of the client."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
