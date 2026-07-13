from decimal import Decimal
import json

from django.db import transaction
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
)
from django.contrib.messages.views import SuccessMessageMixin

from customers.models import Customer
from products.models import Product

from .forms import SaleForm
from .models import Sale, SaleItem


# =====================================================
# AUTO SALE INVOICE NUMBER
# =====================================================

def generate_sale_invoice():

    last = Sale.objects.aggregate(
        Max("id")
    )["id__max"]

    if last:
        next_id = last + 1
    else:
        next_id = 1

    return f"SAL-{next_id:06d}"


# =====================================================
# SALE LIST
# =====================================================

class SaleListView(ListView):

    model = Sale

    template_name = "sales/sale_list.html"

    context_object_name = "sales"

    paginate_by = 10


# =====================================================
# SALE ENTRY SCREEN
# =====================================================

def sale_create(request):

    form = SaleForm(

        initial={

            "invoice_number": generate_sale_invoice(),

            "sale_date": timezone.now().date(),

        }

    )

    return render(

        request,

        "sales/sale_form.html",

        {

            "form": form,

        },

    )
# =====================================================
# PRODUCT DETAILS
# =====================================================

def product_details(request, pk):

    product = get_object_or_404(

        Product,

        pk=pk

    )

    return JsonResponse({

        "id": product.id,

        "barcode": product.barcode,

        "name": product.name,

        "unit": product.unit.short_name,

        "selling_price": float(product.selling_price),

        "gst": float(product.gst_percentage),

        "stock": float(product.current_stock),

    })


# =====================================================
# PRODUCT LIST API
# =====================================================

def product_list_api(request):

    products = Product.objects.filter(

        is_active=True

    ).select_related(

        "unit"

    )

    data = []

    for product in products:

        data.append({

            "id": product.id,

            "barcode": product.barcode,

            "name": product.name,

            "unit": product.unit.short_name,

            "selling_price": float(product.selling_price),

            "gst": float(product.gst_percentage),

            "stock": float(product.current_stock),

        })

    return JsonResponse(

        data,

        safe=False

    )


# =====================================================
# CUSTOMER LIST API
# =====================================================

def customer_list_api(request):

    customers = Customer.objects.filter(

        is_active=True

    ).order_by(

        "name"

    )

    data = []

    for customer in customers:

        data.append({

            "id": customer.id,

            "customer_code": customer.customer_code,

            "name": customer.name,

            "mobile": customer.mobile,

        })

    return JsonResponse(

        data,

        safe=False

    )
# =====================================================
# SAVE SALE (AJAX)
# =====================================================

@require_POST
@transaction.atomic
def save_sale(request):

    try:

        data = json.loads(request.body)

        # -----------------------------------------
        # CREATE SALE
        # -----------------------------------------

        sale = Sale.objects.create(

            invoice_number=generate_sale_invoice(),

            customer_id=data["customer"],

            sale_date=data["sale_date"],

            subtotal=Decimal(str(data["subtotal"])),

            discount=Decimal(str(data["discount"])),

            gst_amount=Decimal(str(data["gst"])),

            grand_total=Decimal(str(data["grand_total"])),

            remarks=data.get("remarks", ""),

        )

        # -----------------------------------------
        # SAVE ITEMS
        # -----------------------------------------

        for row in data["items"]:

            product = Product.objects.get(

                pk=row["product"]

            )

            qty = Decimal(str(row["qty"]))

            if qty <= 0:

                raise Exception(

                    f"Invalid quantity for {product.name}"

                )

            # -----------------------------------------
            # STOCK CHECK
            # -----------------------------------------

            if product.current_stock < qty:

                raise Exception(

                    f"{product.name} has only {product.current_stock} in stock."

                )

            selling_price = Decimal(

                str(row["selling_price"])

            )

            gst_percent = Decimal(

                str(row["gst"])

            )

            amount = qty * selling_price

            gst_amount = (

                amount * gst_percent

            ) / Decimal("100")

            total = amount + gst_amount

            # -----------------------------------------
            # SAVE SALE ITEM
            # -----------------------------------------

            SaleItem.objects.create(

                sale=sale,

                product=product,

                quantity=qty,

                selling_price=selling_price,

                gst_percentage=gst_percent,

                amount=amount,

                gst_amount=gst_amount,

                total=total,

            )

            # -----------------------------------------
            # DEDUCT STOCK
            # -----------------------------------------

            product.current_stock -= qty

            product.save()

        # -----------------------------------------
        # SUCCESS
        # -----------------------------------------

        return JsonResponse({

            "success": True,

            "message": "Sale Saved Successfully"

        })

    except Exception as e:

        return JsonResponse({

            "success": False,

            "message": str(e)

        })
# =====================================================
# SALE UPDATE
# =====================================================

class SaleUpdateView(
    SuccessMessageMixin,
    UpdateView
):

    model = Sale

    form_class = SaleForm

    template_name = "sales/sale_form.html"

    success_url = reverse_lazy(
        "sales:list"
    )

    success_message = "Sale Updated Successfully."

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        sale = self.object

        context["sale_items"] = [
            {
                "product": item.product.id,
                "product_name": item.product.name,
                "barcode": item.barcode,
                "unit": item.unit,
                "qty": float(item.quantity),
                "selling_price": float(item.selling_price),
                "gst": float(item.gst_percentage),
            }
            for item in sale.items.all()
        ]

        return context


# =====================================================
# SALE DELETE
# =====================================================

class SaleDeleteView(

    DeleteView

):

    model = Sale

    template_name = "sales/sale_delete.html"

    success_url = reverse_lazy(

        "sales:list"

    )