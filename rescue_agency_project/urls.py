from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("agencies/", include("agencies.urls")),
    # API urls removed to fix ModuleNotFoundError
    # path("api/", include("agencies.api_urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", RedirectView.as_view(url="/agencies/", permanent=False)),
]
