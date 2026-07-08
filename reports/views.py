from datetime import date

from django.shortcuts import render
from django.db.models import (
    Sum,
    Avg,
    Count,
    F,
    DecimalField,
    ExpressionWrapper,
)

from sales.models import Sale
from purchases.models import Purchase
from products.models import Product, Category
from customers.models import Customer
from suppliers.models import Supplier

# ==========================================================
# SALES REPORT
# ==========================================================

def sales_report(request):

    sales = Sale.objects.select_related(
        "customer"
    ).order_by(
        "-sale_date",
        "-id"
    )

    # -------------------------
    # Filters
    # -------------------------

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    customer = request.GET.get("customer")

    if from_date:
        sales = sales.filter(
            sale_date__gte=from_date
        )

    if to_date:
        sales = sales.filter(
            sale_date__lte=to_date
        )

    if customer:
        sales = sales.filter(
            customer_id=customer
        )

    # -------------------------
    # Totals
    # -------------------------

    totals = sales.aggregate(
        subtotal=Sum("subtotal"),
        discount=Sum("discount"),
        gst=Sum("gst_amount"),
        grand=Sum("grand_total"),
    )

    today_sales = Sale.objects.filter(
        sale_date=date.today()
    ).aggregate(
        total=Sum("grand_total")
    )["total"] or 0

    monthly_sales = Sale.objects.filter(
        sale_date__year=date.today().year,
        sale_date__month=date.today().month
    ).aggregate(
        total=Sum("grand_total")
    )["total"] or 0

    invoice_count = Sale.objects.count()

    average_bill = Sale.objects.aggregate(
        avg=Avg("grand_total")
    )["avg"] or 0

    context = {

        "sales": sales,

        "totals": totals,

        "today_sales": today_sales,

        "monthly_sales": monthly_sales,

        "invoice_count": invoice_count,

        "average_bill": average_bill,

        "customers": Customer.objects.filter(
            is_active=True
        ).order_by("name"),
    }

    return render(
        request,
        "reports/sales_report.html",
        context
    )

def purchase_report(request):

    purchases = Purchase.objects.select_related(
        "supplier"
    ).order_by("-purchase_date", "-id")

    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    supplier = request.GET.get("supplier")

    if from_date:
        purchases = purchases.filter(
            purchase_date__gte=from_date
        )

    if to_date:
        purchases = purchases.filter(
            purchase_date__lte=to_date
        )

    if supplier:
        purchases = purchases.filter(
            supplier_id=supplier
        )

    totals = purchases.aggregate(
        subtotal=Sum("subtotal"),
        discount=Sum("discount"),
        gst=Sum("gst_amount"),
        grand=Sum("grand_total"),
    )

    context = {

        "purchases": purchases,

        "suppliers": Supplier.objects.filter(
            is_active=True
        ),

        "totals": totals,

        "today_purchase": Purchase.objects.filter(
            purchase_date=date.today()
        ).aggregate(
            total=Sum("grand_total")
        )["total"] or 0,

        "monthly_purchase": Purchase.objects.filter(
            purchase_date__year=date.today().year,
            purchase_date__month=date.today().month
        ).aggregate(
            total=Sum("grand_total")
        )["total"] or 0,

        "invoice_count": Purchase.objects.count(),

        "average_bill": Purchase.objects.aggregate(
            avg=Avg("grand_total")
        )["avg"] or 0,
    }

    return render(
        request,
        "reports/purchase_report.html",
        context
    )

def stock_report(request):

    products = Product.objects.select_related(
        "category",
        "unit"
    ).filter(
        is_active=True
    )

    search = request.GET.get("search")
    category = request.GET.get("category")
    status = request.GET.get("status")

    if search:
        products = products.filter(
            name__icontains=search
        )

    if category:
        products = products.filter(
            category_id=category
        )

    if status == "instock":
        products = products.filter(
            current_stock__gt=10
        )

    elif status == "low":
        products = products.filter(
            current_stock__gt=0,
            current_stock__lte=10
        )

    elif status == "out":
        products = products.filter(
            current_stock=0
        )

    stock_value = products.aggregate(
        total=Sum(
            ExpressionWrapper(
                F("current_stock") * F("purchase_price"),
                output_field=DecimalField()
            )
        )
    )["total"] or 0

    context = {

        "products": products,

        "categories": Category.objects.filter(
            is_active=True
        ),

        "total_products": Product.objects.filter(
            is_active=True
        ).count(),

        "low_stock": Product.objects.filter(
            current_stock__gt=0,
            current_stock__lte=10,
            is_active=True
        ).count(),

        "out_stock": Product.objects.filter(
            current_stock=0,
            is_active=True
        ).count(),

        "stock_value": stock_value,
    }

    return render(
        request,
        "reports/stock_report.html",
        context
    )

def customer_report(request):

    customers = Customer.objects.filter(
        is_active=True
    ).annotate(
        total_sales=Count("sales"),
        amount=Sum("sales__grand_total")
    )

    return render(
        request,
        "reports/customer_report.html",
        {
            "customers": customers
        }
    )

def supplier_report(request):

    suppliers = Supplier.objects.filter(
        is_active=True
    ).annotate(
        total_purchase=Count("purchase"),
        amount=Sum("purchase__grand_total")
    )

    return render(
        request,
        "reports/supplier_report.html",
        {
            "suppliers": suppliers
        }
    )
def profit_report(request):

    purchase_total = Purchase.objects.aggregate(
        total=Sum("grand_total")
    )["total"] or 0

    sales_total = Sale.objects.aggregate(
        total=Sum("grand_total")
    )["total"] or 0

    profit = sales_total - purchase_total

    context = {

        "purchase_total": purchase_total,

        "sales_total": sales_total,

        "profit": profit,
    }

    return render(
        request,
        "reports/profit_report.html",
        context
    )