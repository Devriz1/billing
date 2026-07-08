from django.db import models


# ==========================================================
# CATEGORY
# ==========================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
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
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# ==========================================================
# BRAND
# ==========================================================

class Brand(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    description = models.TextField(
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

    def __str__(self):
        return self.name


# ==========================================================
# UNIT
# ==========================================================

class Unit(models.Model):

    name = models.CharField(
        max_length=50
    )

    short_name = models.CharField(
        max_length=10
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.short_name


# ==========================================================
# PRODUCT
# ==========================================================

class Product(models.Model):

    barcode = models.CharField(
        "Barcode",
        max_length=50,
        unique=True,
        blank=True
    )

    name = models.CharField(
        max_length=200
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT
    )

    purchase_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    selling_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # Opening stock while creating product
    opening_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    # Running stock (updated after purchases & sales)
    current_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    minimum_stock = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    gst_enabled = models.BooleanField(
        default=False
    )

    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0
    )

    hsn_code = models.CharField(
        max_length=20,
        blank=True
    )

    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
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

            models.Index(fields=["barcode"]),
            models.Index(fields=["name"]),

        ]

    def save(self, *args, **kwargs):

        # ---------------------------------------
        # AUTO BARCODE
        # ---------------------------------------

        if not self.barcode:

            last_product = Product.objects.order_by("-id").first()

            if last_product and last_product.barcode:

                try:

                    last_number = int(
                        last_product.barcode.replace("EB", "")
                    )

                except ValueError:

                    last_number = last_product.id

                self.barcode = f"EB{last_number + 1:06d}"

            else:

                self.barcode = "EB000001"

        # ---------------------------------------
        # FIRST TIME PRODUCT CREATION
        # ---------------------------------------

        if self.pk is None:

            self.current_stock = self.opening_stock

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.name} ({self.barcode})"