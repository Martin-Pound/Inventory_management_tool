from django.shortcuts import render
from django.views import View
from core.models import Item, Category, Warehouse, Supplier
from django.db.models import Sum
from django.db.models.functions import Coalesce

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
        pass

    def get(self, request):
        return render(request, self.template_name)