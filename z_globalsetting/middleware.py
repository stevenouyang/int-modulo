from django.shortcuts import render
from .models import SiteStatusSetting


class SiteStatusSettingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/admin/") or request.path.startswith("/django-admin/"):
            return self.get_response(request)

        site_status = SiteStatusSetting.load(request_or_site=request)

        if site_status.status == "maintenance":
            return render(request, "general/maintenance.html", status=503)
        elif site_status.status == "coming_soon":
            return render(request, "general/coming-soon.html", status=200)

        return self.get_response(request)
