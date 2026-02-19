from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView

from inventory.error_views import error_404, error_500
from apps.users.views import dashboard

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(url="/dashboard/", permanent=False)),
    path("dashboard/", dashboard, name="dashboard"),
    path("users/", include("apps.users.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("products/", include("apps.products.urls")),
    path("warehouses/", include("apps.warehouses.urls")),
    path("suppliers/", include("apps.suppliers.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("movements/", include("apps.movements.urls")),
    path("audit/", include("apps.audit.urls")),
    path("reports/", include("apps.reports.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

handler404 = error_404
handler500 = error_500
