from django.urls import path
from .views import (
    SupplierListView,
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,
)

app_name = "suppliers"

urlpatterns = [

    path(
        "",
        SupplierListView.as_view(),
        name="list",
    ),

    path(
        "add/",
        SupplierCreateView.as_view(),
        name="add",
    ),

    path(
        "<int:pk>/edit/",
        SupplierUpdateView.as_view(),
        name="edit",
    ),

    path(
        "<int:pk>/delete/",
        SupplierDeleteView.as_view(),
        name="delete",
    ),

]