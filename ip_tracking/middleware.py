import requests
from django.core.cache import cache
from django.http import HttpResponseForbidden
from ipware import get_client_ip
from django.conf import settings
from .models import RequestLog, BlockedIP

def get_geolocation(ip):
    cached = cache.get(f"geo:{ip}")
    if cached:
        return cached

    try:
        response = requests.get(
            "https://api.ipgeolocation.io/ipgeo",
            params={
                "apiKey": settings.IPGEOLOCATION_API_KEY,
                "ip": ip,
                "fields": "country,city"
            },
            timeout=5
        )
        data = response.json()
        geo = {"country": data.get("country"), "city": data.get("city")}
    except Exception:
        geo = {"country": None, "city": None}

    cache.set(f"geo:{ip}", geo, timeout=86400)
    return geo

class IPTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip, _ = get_client_ip(request)

        if ip and BlockedIP.objects.filter(ip_address=ip).exists():
            return HttpResponseForbidden("Access denied")

        country = None
        city = None

        if ip:
            geo = get_geolocation(ip)
            country = geo.get("country")
            city = geo.get("city")

            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                country=country,
                city=city
            )

        response = self.get_response(request)
        return response