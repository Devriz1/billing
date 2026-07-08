from django.urls import path

from . import views

from .views import (

    SaleListView,
    sale_create,
    SaleUpdateView,
    SaleDeleteView,
    product_details,

)

app_name = "sales"

urlpatterns = [

    path(
        "",
        SaleListView.as_view(),
        name="list",
    ),

    path(
        "add/",
        sale_create,
        name="add",
    ),

    path(
        "<int:pk>/edit/",
        SaleUpdateView.as_view(),
        name="edit",
    ),

    path(
        "<int:pk>/delete/",
        SaleDeleteView.as_view(),
        name="delete",
    ),

    path(
        "save/",
        views.save_sale,
        name="save",
    ),

    path(
        "products/",
        views.product_list_api,
        name="products-api",
    ),

    path(
        "customers/",
        views.customer_list_api,
        name="customers-api",
    ),

    path(
        "product/<int:pk>/",
        product_details,
        name="product-details",
    ),

]