# ip_tracking/middleware.py

import time
from django.http import HttpResponseForbidden
from django.core.cache import cache
from .models import RequestLog, BlockedIP

# If using django-ip-geolocation, import the middleware or helper
from django_ip_geolocation.middleware import IpGeolocationMiddleware

class IPLoggingMiddleware:
    """
    Middleware that logs each incoming request, blocks blacklisted IPs,
    and enriches log entries with geolocation (country, city) using caching.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip_address = self.get_client_ip(request)
        path = request.path

        # Block list check
        if BlockedIP.objects.filter(ip_address=ip_address).exists():
            return HttpResponseForbidden("Your IP has been blocked.")

        # Geolocation cache key
        cache_key = f"geo_{ip_address}"
        geo = cache.get(cache_key)

        if not geo:
            # Use the geolocation service to determine location
            # Example using django-ip-geolocation:
            # first ensure request.geolocation exists via its middleware or call manually
            try:
                # If you are using django-ip-geolocation middleware earlier in chain
                geoloc = request.geolocation  
                country = geoloc.country.get("name") if geoloc and geoloc.country else None
                city = geoloc.city or None
            except Exception:
                country = None
                city = None

            # Store in cache for 24h (86400 seconds)
            geo = {"country": country, "city": city}
            cache.set(cache_key, geo, 86400)  # 24h TTL
        else:
            country = geo.get("country")
            city = geo.get("city")

        # Log request
        RequestLog.objects.create(
            ip_address=ip_address,
            path=path,
            country=country,
            city=city
        )

        # Continue processing
        response = self.get_response(request)
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip




