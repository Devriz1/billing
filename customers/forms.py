from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:

        model = Customer

        fields = [

            "customer_code",
            "name",
            "mobile",
            "whatsapp",
            "email",
            "gstin",
            "pan_number",
            "contact_person",
            "address1",
            "address2",
            "city",
            "state",
            "country",
            "pincode",
            "opening_balance",
            "credit_limit",
            "payment_terms",
            "customer_type",
            "notes",
            "is_active",

        ]

        widgets = {

            "customer_code": forms.TextInput(attrs={
                "class": "form-control",
                "readonly": True
            }),

            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Customer Name"
            }),

            "mobile": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Mobile Number"
            }),

            "whatsapp": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "WhatsApp Number"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email Address"
            }),

            "gstin": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "GST Number"
            }),

            "pan_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "PAN Number"
            }),

            "contact_person": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Contact Person"
            }),

            "address1": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Address Line 1"
            }),

            "address2": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Address Line 2"
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "country": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "pincode": forms.TextInput(attrs={
                "class": "form-control"
            }),

            "opening_balance": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "credit_limit": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01"
            }),

            "payment_terms": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "customer_type": forms.Select(attrs={
                "class": "form-select"
            }),

            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),

        }