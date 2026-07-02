from django.urls import path
from .views import (
    PurchaseListView,
    purchase_create,
    PurchaseUpdateView,
    PurchaseDeleteView,
)

app_name = "purchases"

urlpatterns = [

    path(
        "",
        PurchaseListView.as_view(),
        name="list",
    ),

   path(
    "add/",
    purchase_create,
    name="add",
),

    path(
        "<int:pk>/edit/",
        PurchaseUpdateView.as_view(),
        name="edit",
    ),

    path(
        "<int:pk>/delete/",
        PurchaseDeleteView.as_view(),
        name="delete",
    ),
]