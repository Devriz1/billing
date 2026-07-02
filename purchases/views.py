from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, redirect
from .models import Purchase
from .forms import PurchaseForm, PurchaseItemFormSet
from django.contrib import messages


class PurchaseListView(ListView):
    model = Purchase
    template_name = "purchases/purchase_list.html"
    context_object_name = "purchases"
    paginate_by = 10


def purchase_create(request):

    if request.method == "POST":

        form = PurchaseForm(request.POST)

        formset = PurchaseItemFormSet(request.POST)

        if form.is_valid() and formset.is_valid():

            purchase = form.save()

            items = formset.save(commit=False)

            subtotal = 0

            for item in items:

                item.purchase = purchase

                item.total = item.quantity * item.purchase_price

                subtotal += item.total

                item.save()

            purchase.subtotal = subtotal

            gst_amount = (
                subtotal - purchase.discount
            ) * purchase.gst_percentage / 100

            purchase.tax = gst_amount

            purchase.grand_total = (
                subtotal
                - purchase.discount
                + gst_amount
)

            purchase.save()

            messages.success(
                request,
                "Purchase saved successfully."
            )

            return redirect("purchases:list")

    else:

        form = PurchaseForm()

        formset = PurchaseItemFormSet()

    return render(
        request,
        "purchases/purchase_form.html",
        {
            "form": form,
            "formset": formset,
        },
    )

class PurchaseUpdateView(SuccessMessageMixin, UpdateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = "purchases/purchase_form.html"
    success_url = reverse_lazy("purchases:list")
    success_message = "Purchase updated successfully."


class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = "purchases/purchase_delete.html"
    success_url = reverse_lazy("purchases:list")