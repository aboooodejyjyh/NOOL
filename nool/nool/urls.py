from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("inventory/", include("inventory.urls", namespace="inventory")),
    path("pos/", include("pos.urls", namespace="pos")),
    path("sales/", include("sales.urls", namespace="sales")),
    path("", RedirectView.as_view(url="/inventory/"), name="home"),
]
