from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Max, Q
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    UpdateView,
    DeleteView,
)

from .forms import CustomerForm
from .models import Customer


# ===========================================
# Generate Customer Code
# ===========================================

def generate_customer_code():

    last = Customer.objects.aggregate(
        Max("id")
    )["id__max"]

    if last:

        next_id = last + 1

    else:

        next_id = 1

    return f"CUS{next_id:06d}"


# ===========================================
# Customer List
# ===========================================



class CustomerListView(ListView):

    model = Customer
    template_name = "customers/customer_list.html"
    context_object_name = "customers"
    paginate_by = 15

    def get_queryset(self):

        queryset = Customer.objects.all()

        q = self.request.GET.get("q")

        if q:

            queryset = queryset.filter(

                Q(customer_code__icontains=q) |
                Q(name__icontains=q) |
                Q(mobile__icontains=q) |
                Q(city__icontains=q)

            )

        return queryset.order_by("name")
# ===========================================
# Add Customer
# ===========================================

def customer_create(request):

    if request.method == "POST":

        form = CustomerForm(request.POST)

        if form.is_valid():

            customer = form.save()

            # Popup support

            if request.GET.get("popup"):

                return render(

                    request,

                    "customers/popup_close.html",

                    {

                        "customer": customer

                    }

                )

            messages.success(

                request,

                "Customer Added Successfully."

            )

            return redirect("customers:list")

    else:

        form = CustomerForm(

            initial={

                "customer_code": generate_customer_code()

            }

        )

    return render(

        request,

        "customers/customer_form.html",

        {

            "form": form

        }

    )


# ===========================================
# Edit Customer
# ===========================================

class CustomerUpdateView(

    SuccessMessageMixin,

    UpdateView

):

    model = Customer

    form_class = CustomerForm

    template_name = "customers/customer_form.html"

    success_url = reverse_lazy("customers:list")

    success_message = "Customer Updated Successfully."


# ===========================================
# Delete Customer
# ===========================================

class CustomerDeleteView(DeleteView):

    model = Customer

    template_name = "customers/customer_delete.html"

    success_url = reverse_lazy("customers:list")