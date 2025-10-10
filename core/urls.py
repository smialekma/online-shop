from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("", include("products.urls")),
    path("", include("customers.urls")),
    path("", include("orders.urls")),
    path("", include("payments.urls")),
    path("", include("customer_addresses.urls")),
    path("management/", include("management_panel.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += debug_toolbar_urls()
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
