from django import forms
from .models import Category, Unit, Product


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = [
            "name",
            "description",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter category name"
            }),

            "description": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Description"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }


class UnitForm(forms.ModelForm):

    class Meta:
        model = Unit

        fields = [
            "name",
            "short_name",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter unit name"
            }),

            "short_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Eg: Kg, Pc, Ltr"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product

        fields = [
            "barcode",
            "name",
            "category",
            "unit",
            "purchase_price",
            "selling_price",
            "opening_stock",
            "minimum_stock",
            "gst_enabled",
            "gst_percentage",
            "hsn_code",
            "image",
            "is_active",
        ]

        widgets = {
            "barcode": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Barcode"
            }),

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Product Name"
            }),

            "category": forms.Select(attrs={
                "class": "form-select"
            }),

            "unit": forms.Select(attrs={
                "class": "form-select"
            }),

            "purchase_price": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "selling_price": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "opening_stock": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "minimum_stock": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "gst_enabled": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

            "gst_percentage": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "hsn_code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "HSN Code"
            }),

            "image": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        purchase = cleaned_data.get("purchase_price")
        selling = cleaned_data.get("selling_price")
        gst_enabled = cleaned_data.get("gst_enabled")
        gst_percentage = cleaned_data.get("gst_percentage")

        if (
            purchase is not None
            and selling is not None
            and selling < purchase
        ):
            self.add_error(
                "selling_price",
                "Selling price cannot be less than purchase price."
            )

        if (
            gst_enabled
            and gst_percentage is not None
            and gst_percentage <= 0
        ):
            self.add_error(
                "gst_percentage",
                "Enter a valid GST percentage."
            )

        return cleaned_data