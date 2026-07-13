from decimal import Decimal
import json
from django.db.models import Max
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView, ListView, UpdateView

from products.models import Product
from .forms import PurchaseForm
from .models import Purchase, PurchaseItem


# ===========================================================
# PURCHASE LIST
# ===========================================================

class PurchaseListView(ListView):
    model = Purchase
    template_name = "purchases/purchase_list.html"
    context_object_name = "purchases"
    paginate_by = 10


# ===========================================================
# PURCHASE ENTRY SCREEN
# ===========================================================
def generate_purchase_invoice():

    last = Purchase.objects.aggregate(
        Max("id")
    )["id__max"]

    if last:

        next_id = last + 1

    else:

        next_id = 1

    return f"PUR-{next_id:06d}"


def purchase_create(request):

    form = PurchaseForm(

        initial={

            "invoice_number": generate_purchase_invoice(),

            "purchase_date": timezone.now().date(),

        }

    )

    return render(

        request,

        "purchases/purchase_form.html",

        {

            "form": form,

        },

    )

# ===========================================================
# SAVE PURCHASE (AJAX)
# ===========================================================

@require_POST
@transaction.atomic
def save_purchase(request):

    try:

        data = json.loads(request.body)

        purchase = Purchase.objects.create(

    invoice_number=generate_purchase_invoice(),

    supplier_id=data["supplier"],

    purchase_date=data["purchase_date"],

    subtotal=0,

    discount=Decimal(str(data["discount"])),

    tax=0,

    grand_total=0,

    remarks=data.get("remarks", ""),

)

        for row in data["items"]:

            product = Product.objects.get(pk=row["product"])

            PurchaseItem.objects.create(

                purchase=purchase,

                product=product,

                quantity=Decimal(str(row["qty"])),

                purchase_price=Decimal(str(row["purchase_price"])),

                gst_percentage=Decimal(str(row["gst"])),

                selling_price=Decimal(str(row["selling_price"])),

            )

            # Update stock

            product.current_stock += Decimal(str(row["qty"]))

            product.purchase_price = Decimal(str(row["purchase_price"]))

            product.selling_price = Decimal(str(row["selling_price"]))

            product.gst_percentage = Decimal(str(row["gst"]))

            product.save()

            subtotal = Decimal("0")
            gst_total = Decimal("0")

            for item in purchase.items.all():

                subtotal += item.quantity * item.purchase_price

                gst_total += item.gst_amount

            purchase.subtotal = subtotal

            purchase.tax = gst_total

            purchase.grand_total = (

                subtotal

                - purchase.discount

                + gst_total

            )

            purchase.save()

        return JsonResponse({
            "success": True,
            "message": "Purchase Saved Successfully"
        })

    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        })


# ===========================================================
# UPDATE
# ===========================================================

class PurchaseUpdateView(SuccessMessageMixin, UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchase_form.html"
    success_url = reverse_lazy("purchases:list")
    success_message = "Purchase updated successfully."

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        purchase = self.object

        context["purchase_items"] = [
            {
                "product": item.product.id,
                "product_name": item.product.name,
                "barcode": item.barcode,
                "unit": item.unit,
                "qty": float(item.quantity),
                "purchase_price": float(item.purchase_price),
                "selling_price": float(item.selling_price),
                "gst": float(item.gst_percentage),
            }
            for item in purchase.items.all()
        ]

        return context
# ===========================================================
# DELETE
# ===========================================================

class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = "purchases/purchase_delete.html"
    success_url = reverse_lazy("purchases:list")


# ===========================================================
# PRODUCT DETAILS
# ===========================================================

def product_details(request, pk):

    product = get_object_or_404(Product, pk=pk)

    return JsonResponse({

        "id": product.id,
        "barcode": product.barcode,
        "name": product.name,
        "unit": product.unit.short_name,
        "purchase_price": float(product.purchase_price),
        "selling_price": float(product.selling_price),
        "gst_percentage": float(product.gst_percentage),

    })


# ===========================================================
# PRODUCT API
# ===========================================================

def product_list_api(request):

    products = Product.objects.select_related(
        "category",
        "unit"
    ).filter(
        is_active=True
    )

    data = []

    for product in products:

        data.append({

    "id": product.id,
    "barcode": product.barcode,
    "name": product.name,
    "unit": product.unit.short_name,
    "purchase_price": float(product.purchase_price),
    "selling_price": float(product.selling_price),
    "gst": float(product.gst_percentage),

})

    return JsonResponse(data, safe=False)