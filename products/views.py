from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from products.models import Product, Category
from .models import Category, Unit, Product
from .forms import CategoryForm, UnitForm, ProductForm


# =====================================================
# CATEGORY VIEWS
# =====================================================

class CategoryListView(ListView):
    model = Category
    template_name = "products/category_list.html"
    context_object_name = "categories"
    paginate_by = 10

    def get_queryset(self):
        queryset = Category.objects.all()

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset


class CategoryCreateView(SuccessMessageMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("products:category_list")
    success_message = "Category created successfully."


class CategoryUpdateView(SuccessMessageMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "products/category_form.html"
    success_url = reverse_lazy("products:category_list")
    success_message = "Category updated successfully."


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "products/category_delete.html"
    success_url = reverse_lazy("products:category_list")


# =====================================================
# UNIT VIEWS
# =====================================================

class UnitListView(ListView):
    model = Unit
    template_name = "products/unit_list.html"
    context_object_name = "units"
    paginate_by = 10

    def get_queryset(self):
        queryset = Unit.objects.all()

        search = self.request.GET.get("search")

        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(short_name__icontains=search)
            )

        return queryset


class UnitCreateView(SuccessMessageMixin, CreateView):
    model = Unit
    form_class = UnitForm
    template_name = "products/unit_form.html"
    success_url = reverse_lazy("products:unit_list")
    success_message = "Unit created successfully."


class UnitUpdateView(SuccessMessageMixin, UpdateView):
    model = Unit
    form_class = UnitForm
    template_name = "products/unit_form.html"
    success_url = reverse_lazy("products:unit_list")
    success_message = "Unit updated successfully."


class UnitDeleteView(DeleteView):
    model = Unit
    template_name = "products/unit_delete.html"
    success_url = reverse_lazy("products:unit_list")


# =====================================================
# PRODUCT VIEWS
# =====================================================

def product_list(request):

    products = Product.objects.all()

    search = request.GET.get("search")

    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(barcode__icontains=search) |
            Q(category__name__icontains=search)
        )

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "search": search,
        },
    )


def product_create(request):

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():

            print("========== FORM IS VALID ==========")

            product = form.save()

            print("Product ID:", product.id)
            print("Popup:", request.GET.get("popup"))

            # Opened from Purchase Screen
            if request.GET.get("popup") == "1":

                print("========== POPUP MODE ==========")

                return render(
                    request,
                    "products/product_popup_success.html",
                    {
                        "product_id": product.id,
                    },
                )

            print("========== NORMAL MODE ==========")

            return redirect("products:list")

        else:

            print("========== FORM ERRORS ==========")
            print(form.errors)

    else:

        form = ProductForm()

    return render(
        request,
        "products/product_form.html",
        {
            "form": form,
            "title": "Add Product",
        },
    )

def product_update(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":

        form = ProductForm(
            request.POST,
            request.FILES,
            instance=product,
        )

        if form.is_valid():

            form.save()

            return redirect("products:list")

    else:

        form = ProductForm(instance=product)

    return render(
        request,
        "products/product_form.html",
        {
            "form": form,
            "title": "Edit Product",
        },
    )


def product_delete(request, pk):

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":

        product.delete()

        return redirect("products:list")

    return render(
        request,
        "products/product_delete.html",
        {
            "product": product,
        },
    )