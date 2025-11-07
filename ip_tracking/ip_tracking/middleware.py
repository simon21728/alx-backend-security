# ip_tracking/middleware.py

class IPLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Example: log the IP address
        ip = request.META.get('REMOTE_ADDR')
        print(f"Visitor IP: {ip}")
        response = self.get_response(request)
        return response
