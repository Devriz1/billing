from django.contrib import admin
from .models import Business


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner_name",
        "phone",
        "gst_enabled",
        "barcode_enabled",
        "is_active",
    )

    search_fields = (
        "name",
        "phone",
        "owner_name",
    )

    list_filter = (
        "gst_enabled",
        "barcode_enabled",
        "is_active",
    )