from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "customer_code",
        "name",
        "mobile",
        "city",
        "opening_balance",
        "credit_limit",
        "is_active",
    )

    search_fields = (
        "customer_code",
        "name",
        "mobile",
        "email",
        "gstin",
    )

    list_filter = (
        "is_active",
        "customer_type",
        "city",
        "state",
    )

    ordering = (
        "name",
    )

    list_per_page = 25