from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [

    path(
        "sales/",
        views.sales_report,
        name="sales",
    ),

    path(
        "purchase/",
        views.purchase_report,
        name="purchase",
    ),

    path(
        "stock/",
        views.stock_report,
        name="stock",
    ),

    path(
        "customer/",
        views.customer_report,
        name="customer",
    ),

    path(
        "supplier/",
        views.supplier_report,
        name="supplier",
    ),

    path(
        "profit/",
        views.profit_report,
        name="profit",
    ),

]