from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("products/",include("products.urls")),
    path("suppliers/", include("suppliers.urls")),
    path("purchases/", include("purchases.urls")),
    path("select2/", include("django_select2.urls")),
    path("customers/", include("customers.urls")),
    path("sales/", include("sales.urls")),
    path("reports/",include("reports.urls"),),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)