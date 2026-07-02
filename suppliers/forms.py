from django import forms
from .models import Supplier


class SupplierForm(forms.ModelForm):

    class Meta:
        model = Supplier

        fields = [
            "name",
            "contact_person",
            "phone",
            "email",
            "gst_number",
            "address",
            "city",
            "state",
            "pincode",
            "opening_balance",
            "is_active",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Supplier Name"
            }),

            "contact_person": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Contact Person"
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Phone Number"
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Email Address"
            }),

            "gst_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "GST Number"
            }),

            "address": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Address"
            }),

            "city": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "City"
            }),

            "state": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "State"
            }),

            "pincode": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Pincode"
            }),

            "opening_balance": forms.NumberInput(attrs={
                "class": "form-control"
            }),

            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]

        if len(phone) < 10:
            raise forms.ValidationError(
                "Phone number must contain at least 10 digits."
            )

        return phone