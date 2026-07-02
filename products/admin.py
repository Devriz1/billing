from django.contrib import admin
from .models import Category, Unit, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name", "is_active")
    search_fields = ("name", "short_name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "barcode",
        "name",
        "category",
        "unit",
        "purchase_price",
        "selling_price",
        "opening_stock",
        "is_active",
    )

    search_fields = (
        "name",
        "barcode",
    )

    list_filter = (
        "category",
        "unit",
        "is_active",
    )