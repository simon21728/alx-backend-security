from django.shortcuts import render
# ip_tracking/views.py

from django.http import HttpResponse
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST', block=True)
@ratelimit(key='ip', rate='10/m', method='GET', block=False)
def login_view(request):
    """
    A simple example login view protected by rate limiting.
    Anonymous users: 5 requests/minute (block on exceed)
    Authenticated users: 10 requests/minute (warn or block if needed)
    """
    if request.user.is_authenticated:
        return HttpResponse("Welcome back! You’re authenticated.")
    return HttpResponse("Login page – anonymous user.")
