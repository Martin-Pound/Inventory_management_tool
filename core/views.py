from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from core.forms import WarehouseForm, BinForm, CatergoryForm, SupplierForm
from core.models import Item, Category, Warehouse, Supplier, Bin
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse



# Create your views here.
class DashboardView(View):
    template_name = "core/index.html"

    def get_category_summaries(self):
        return (
            Category.objects
            .annotate(total_quantity=Coalesce(Sum("items__stock_levels__quantity"), 0))
            .order_by("-total_quantity")
        )

    def get_warehouse_summaries(self):
        return (
            Warehouse.objects
            .annotate(total_quantity=Coalesce(Sum("bins__stock_levels__quantity"), 0))
            .order_by("-total_quantity")
        )

    def supplier_summaries(self):
        return (
            Supplier.objects
            .annotate(total_quantity=Coalesce(Sum("items__stock_levels__quantity"), 0))
            .order_by("-total_quantity")
        )

    def get(self, request):
        context = {
            "category_summaries": self.get_category_summaries(),
            "warehouse_summaries": self.get_warehouse_summaries(),
            "supplier_summaries": self.supplier_summaries(),
        }
        return render(request, self.template_name, context)

class ConfigureView(View):
    template_name = "core/configure.html"

    def bin_form(self):
        return BinForm()

    def category_form(self):
        return CatergoryForm

    def supplier_form(self):
        return SupplierForm

    def warehouse_form(self):
        return WarehouseForm()

    def item_form(self):
        pass

    def get(self, request):
        context = {
            "bin_form": self.bin_form(),
            "warehouse_form": self.warehouse_form(),
            "category_form": self.category_form(),
        }
        return render(request, self.template_name, context)

    def post(self,
            request):
        # Check which form was submitted (if you have multiple forms)
        form_type = request.POST.get('form_type', '')

        # Handle warehouse form
        if form_type == 'warehouse':
            warehouse_form = WarehouseForm(request.POST)
            if warehouse_form.is_valid():
                warehouse = warehouse_form.save()
                messages.success(request, f"Warehouse '{warehouse.warehouse_name}' saved successfully!")
                return HttpResponseRedirect(reverse("configure-page"))
            else:
                context = {
                    "warehouse_form": warehouse_form,
                }
                return render(request, self.template_name, context)

        # Handle bin form
        if form_type == 'bin':
            bin_form = BinForm(request.POST)
            if bin_form.is_valid():
                bin_instance = bin_form.save()
                messages.success(request, f"Bin '{bin_instance.bin_name}' saved successfully!")
                return HttpResponseRedirect(reverse("configure-page"))
            else:
                context = {
                    "bin_form": bin_form,
                }
                return render(request, self.template_name, context)

        #Handle category form
        if form_type == 'category':
            category_form = CatergoryForm(request.POST)
            if category_form.is_valid():
                category = category_form.save()
                messages.success(request, f"Category '{category.category_name}' saved successfully!")
                return HttpResponseRedirect(reverse("configure-page"))
            else:
                context = {
                    "category_form": category_form,
                }
                return render(request, self.template_name, context)

        #Handle supplier form
        if form_type == 'supplier':
            supplier_form = SupplierForm(request.POST)
            if supplier_form.is_valid():
                supplier = supplier_form.save()
                messages.success(request, f"Supplier '{supplier.supplier_name}' saved successfully!")
                return HttpResponseRedirect(reverse("configure-page"))
            else:
                context = {
                    "supplier_form": supplier_form,
                }
                return render(request, self.template_name, context)

        # If we got here, something went wrong
        messages.error(request, "Form submission error")
        return redirect('configure')


