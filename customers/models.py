from django.db import models


class Customer(models.Model):

    customer_code = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    name = models.CharField(
        max_length=200
    )

    mobile = models.CharField(
        max_length=15,
        blank=True
    )

    whatsapp = models.CharField(
        max_length=15,
        blank=True
    )

    email = models.EmailField(
        blank=True
    )

    gstin = models.CharField(
        max_length=20,
        blank=True
    )

    pan_number = models.CharField(
        max_length=20,
        blank=True
    )

    contact_person = models.CharField(
        max_length=100,
        blank=True
    )

    address1 = models.CharField(
        max_length=255,
        blank=True
    )

    address2 = models.CharField(
        max_length=255,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        default="India"
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    opening_balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    credit_limit = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    payment_terms = models.PositiveIntegerField(
        default=0,
        help_text="Credit Days"
    )

    CUSTOMER_TYPES = (

        ("Retail", "Retail"),
        ("Wholesale", "Wholesale"),

    )

    customer_type = models.CharField(
        max_length=20,
        choices=CUSTOMER_TYPES,
        default="Retail"
    )

    notes = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        ordering = ["name"]

        indexes = [

            models.Index(fields=["customer_code"]),
            models.Index(fields=["name"]),
            models.Index(fields=["mobile"]),

        ]

    def save(self, *args, **kwargs):

        if not self.customer_code:

            last = Customer.objects.order_by("-id").first()

            if last and last.customer_code:

                try:

                    number = int(
                        last.customer_code.replace("CUS", "")
                    )

                except ValueError:

                    number = last.id

                self.customer_code = f"CUS{number+1:06d}"

            else:

                self.customer_code = "CUS000001"

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.customer_code} - {self.name}"