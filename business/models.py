from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    logo = models.ImageField(
        upload_to="business/logo/",
        blank=True,
        null=True,
    )

    currency = models.CharField(max_length=10, default="INR")
    currency_symbol = models.CharField(max_length=5, default="₹")

    gst_enabled = models.BooleanField(default=False)
    gst_number = models.CharField(max_length=20, blank=True)

    barcode_enabled = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "business"
        ordering = ["name"]

    def __str__(self):
        return self.name