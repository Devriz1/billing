from django import forms
from django.forms import inlineformset_factory
from .models import Purchase, PurchaseItem


class PurchaseForm(forms.ModelForm):

    class Meta:
        model = Purchase

        fields = [
    "invoice_number",
    "supplier",
    "purchase_date",
    "discount",
    "gst_percentage",
    "remarks",
]

        widgets = {
            "invoice_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Invoice Number"
            }),

            "supplier": forms.Select(attrs={
                "class": "form-select"
            }),

            "purchase_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "discount": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "tax": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "gst_percentage": forms.NumberInput(attrs={
    "class": "form-control",
    "placeholder": "GST %"
}),
        }


class PurchaseItemForm(forms.ModelForm):

    class Meta:
        model = PurchaseItem

        fields = [
            "product",
            "quantity",
            "purchase_price",
        ]

        widgets = {
            "product": forms.Select(attrs={
                "class": "form-select"
            }),

            "quantity": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "purchase_price": forms.NumberInput(attrs={
                "class": "form-control"
            }),
        }

PurchaseItemFormSet = inlineformset_factory(
    Purchase,
    PurchaseItem,
    form=PurchaseItemForm,
    extra=1,
    can_delete=True
)