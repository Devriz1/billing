from django.urls import path
from . import views
from .views import (
    PurchaseListView,
    purchase_create,
    PurchaseUpdateView,
    PurchaseDeleteView,
    product_details,
)

app_name = "purchases"

urlpatterns = [

    # Purchase List
    path(
        "",
        PurchaseListView.as_view(),
        name="list",
    ),

    # Add Purchase
    path(
        "add/",
        purchase_create,
        name="add",
    ),

    # Edit Purchase
    path(
        "<int:pk>/edit/",
        PurchaseUpdateView.as_view(),
        name="edit",
    ),

    # Delete Purchase
    path(
        "<int:pk>/delete/",
        PurchaseDeleteView.as_view(),
        name="delete",
    ),

    # Get Product Details
    path(
        "product/<int:pk>/",
        product_details,
        name="product_details",
    ),
    path(
    "save/",
    views.save_purchase,
    name="save",
),

    # Product API for Purchase Screen
    path(
        "products/",
        views.product_list_api,
        name="products-api",
    ),

    
]