from decimal import Decimal
from django.db import models
from customers.models import Customer
from products.models import Product


class Sale(models.Model):

    invoice_number = models.CharField(
        max_length=30,
        unique=True
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sales"
    )

    sale_date = models.DateField()

    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    discount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    grand_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        ordering = ["-id"]

    def __str__(self):

        return self.invoice_number


class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT
    )

    barcode = models.CharField(
        max_length=50,
        blank=True
    )

    product_name = models.CharField(
        max_length=200
    )

    unit = models.CharField(
        max_length=20
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:

        ordering = ["id"]

    def save(self, *args, **kwargs):

        self.barcode = self.product.barcode
        self.product_name = self.product.name
        self.unit = self.product.unit.short_name

        self.amount = Decimal(self.quantity) * Decimal(self.selling_price)

        self.gst_amount = (
            self.amount * Decimal(self.gst_percentage)
        ) / Decimal("100")

        self.total = self.amount + self.gst_amount

        super().save(*args, **kwargs)

    def __str__(self):

        return self.product_name