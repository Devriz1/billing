from django.urls import path

from .views import (
    CustomerListView,
    customer_create,
    CustomerUpdateView,
    CustomerDeleteView,
)

app_name = "customers"

urlpatterns = [

    # Customer List
    path(
        "",
        CustomerListView.as_view(),
        name="list",
    ),

    # Add Customer
    path(
        "add/",
        customer_create,
        name="add",
    ),

    # Edit Customer
    path(
        "<int:pk>/edit/",
        CustomerUpdateView.as_view(),
        name="edit",
    ),

    # Delete Customer
    path(
        "<int:pk>/delete/",
        CustomerDeleteView.as_view(),
        name="delete",
    ),

]