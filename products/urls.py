from django.urls import path
from . import views
from .views import (
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
UnitListView,
UnitCreateView,
UnitUpdateView,
UnitDeleteView,
)

app_name = "products"

urlpatterns = [
    path(
        "categories/",
        CategoryListView.as_view(),
        name="category_list",
    ),

    path(
        "categories/add/",
        CategoryCreateView.as_view(),
        name="category_add",
    ),

    path(
        "categories/<int:pk>/edit/",
        CategoryUpdateView.as_view(),
        name="category_edit",
    ),

    path(
        "categories/<int:pk>/delete/",
        CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    
path(
    "units/",
    UnitListView.as_view(),
    name="unit_list",
),

path(
    "units/add/",
    UnitCreateView.as_view(),
    name="unit_add",
),

path(
    "units/<int:pk>/edit/",
    UnitUpdateView.as_view(),
    name="unit_edit",
),

path(
    "units/<int:pk>/delete/",
    UnitDeleteView.as_view(),
    name="unit_delete",
),
# Products
path(
    "",
    views.product_list,
    name="list",
),

path(
    "add/",
    views.product_create,
    name="add",
),

path(
    "<int:pk>/edit/",
    views.product_update,
    name="edit",
),

path(
    "<int:pk>/delete/",
    views.product_delete,
    name="delete",
),
]