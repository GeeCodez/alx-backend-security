from django.http import HttpResponseForbidden
from ipware import get_client_ip
from .models import RequestLog, BlockedIP

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)

        # Block if IP is blacklisted
        if ip and BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied")

        # Log the request
        if ip:
            RequestLog.objects.create(ip_address=ip, path=request.path)

        response = self.get_response(request)
        return response
