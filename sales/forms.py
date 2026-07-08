from django import forms
from .models import Sale


class SaleForm(forms.ModelForm):

    class Meta:

        model = Sale

        fields = [

            "invoice_number",
            "customer",
            "sale_date",
            "discount",
            "remarks",

        ]

        widgets = {

            "invoice_number": forms.TextInput(attrs={
                "class": "form-control",
                "readonly": True,
            }),

            "customer": forms.Select(attrs={
                "class": "form-select",
            }),

            "sale_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),

            "discount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "value": 0,
            }),

            "remarks": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
            }),

        }