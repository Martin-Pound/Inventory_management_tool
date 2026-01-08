from statistics import quantiles
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from core.forms import WarehouseForm, BinForm, CategoryForm, SupplierForm, ItemForm
from core.models import Item, Category, Warehouse, Supplier, Bin, StockLevel, MovementType, MovementLog
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.db import models

#Utility functions here
def get_warehouse_bin_matrix(item_id=None):
    """
    Generates a matrix mapping stock levels to its respective bin and warehouses.
    If item_id is provided, only shows stock for that specific item.
    """
    # Get all warehouses columns
    warehouses = Warehouse.objects.order_by("warehouse_name")

    # Base query for stock data
    stock_query = StockLevel.objects

    # Filter by item if provided
    if item_id:
        stock_query = stock_query.filter(item_id=item_id)

    # Get stock data grouped by bin and warehouse
    stock_summary = stock_query.values(
        'bin__id',
        'bin__bin_name',
        'bin__warehouse__id',
        'bin__warehouse__warehouse_name'
    ).annotate(
        total_quantity=Sum('quantity')
    ).order_by('bin__warehouse__warehouse_name', 'bin__bin_name')

    # Build a nested dictionary for easy lookup
    bins_dict = {}

    for item in stock_summary:
        bin_id = item['bin__id']
        bin_name = item['bin__bin_name']
        warehouse_id = item['bin__warehouse__id']
        total = item['total_quantity'] or 0

        if bin_id not in bins_dict:
            bins_dict[bin_id] = {
                'id': bin_id,
                'name': bin_name,
                'warehouses_stocks': {}
            }

        bins_dict[bin_id]['warehouses_stocks'][warehouse_id] = total

    matrix = {
        'warehouses': list(warehouses),
        'bins': [],
        'column_totals': [0] * len(warehouses),
        'grand_total': 0
    }

    # Convert bins_dict to list for template rendering
    for bin_id, bin_data in sorted(bins_dict.items(), key=lambda x: x[1]['name']):
        bin_row = {
            'bin_name': bin_data['name'],
            'quantities': []
        }

        row_total = 0
        for i, warehouse in enumerate(warehouses):
            quantity = bin_data['warehouses_stocks'].get(warehouse.id, 0)
            bin_row['quantities'].append(quantity)
            row_total += quantity
            matrix['column_totals'][i] += quantity

        bin_row['row_total'] = row_total
        matrix['grand_total'] += row_total
        matrix['bins'].append(bin_row)

    return matrix

def get_movement_logs(item_id):
    """
    Fetches movement logs for a specific item.
    """
    queryset = MovementLog.objects.order_by('-date_moved')
    if item_id:
        queryset = queryset.filter(item_id=item_id)
        print(queryset.query)

    return queryset

# Create your views here.
class DashboardView(View):
    template_name = "core/index.html"

    def get_category_summaries(self):
        # Annotate each category with the total quantity of items in that category
        return (
            Category.objects
            .annotate(total_quantity=Coalesce(Sum("items__stock_levels__quantity"), 0))
            .order_by("-total_quantity")
        )

    def get_warehouse_summaries(self):
        # Annotate each warehouse with the total quantity of items stored in that warehouse
        return (
            Warehouse.objects
            .annotate(total_quantity=Coalesce(Sum("bins__stock_levels__quantity"), 0))
            .order_by("-total_quantity")
        )

    def supplier_summaries(self):
        # Annotate each supplier with the total quantity of items supplied by that supplier
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
        return CategoryForm

    def supplier_form(self):
        return SupplierForm

    def warehouse_form(self):
        return WarehouseForm()

    def item_form(self):
        return ItemForm()

    def get(self, request):
        context = {
            "bin_form": self.bin_form(),
            "warehouse_form": self.warehouse_form(),
            "category_form": self.category_form(),
            "supplier_form": self.supplier_form(),
            "item_form": self.item_form(),
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
            category_form = CategoryForm(request.POST)
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

        #Handle item form
        if form_type == 'item':
            item_form = ItemForm(request.POST)
            if item_form.is_valid():
                item = item_form.save()
                messages.success(request, f"Item '{item.item_name}' saved successfully!")
                return HttpResponseRedirect(reverse("configure-page"))
            else:
                context = {
                    "item_form": item_form,
                }
                return render(request, self.template_name, context)

        # If we got here, something went wrong
        messages.error(request, "Form submission error")
        return HttpResponseRedirect(reverse("configure-page"))

class ItemsLookupView(View):
    template_name = "core/item_lookup.html"

    def get_item_details(self, query):
        """
        Fetches detailed information about a specific item based on a search query.
        The search can be by SKU or item name.
        """
        if not query:
            return None

        # Try to find item by SKU (exact match) or name (contains)
        item = Item.objects.filter(
            models.Q(SKU__iexact=query) |
            models.Q(item_name__icontains=query)
        ).first()

        return item

    def get(self, request, *args, **kwargs):
        context = {}

        # Handle item search
        search_query = request.GET.get('q', '')
        if search_query:
            item = self.get_item_details(search_query)
            context['item'] = item

            # If item found, get stock levels for this specific item
            if item:
                # ... existing code ...
                bin_warehouse_matrix = get_warehouse_bin_matrix(item_id=item.id)
                context.update({
                    'bin_warehouse_matrix': bin_warehouse_matrix,
                    # ... other context items
                })

            else:
                # Item not found
                context['search_error'] = f"No items found matching '{search_query}'"
                # Show full matrix if no specific item
                context['bin_warehouse_matrix'] = get_warehouse_bin_matrix()
        else:
            # Show full matrix if no search
            context['bin_warehouse_matrix'] = get_warehouse_bin_matrix()

        return render(request, self.template_name, context)

class ProblemSolveView(View):
    template_name = "core/problem_solve.html"

    def get(self, request, *args, **kwargs):

        search_sku = request.GET.get("search_sku")

        context = {
            'search_form': True
        }

        if search_sku:
            try:
                item = Item.objects.get(SKU__iexact=search_sku)
                form = ItemForm(instance=item)

                # Use the shared function
                bin_warehouse_matrix = get_warehouse_bin_matrix(item_id=item.id)

                movement_logs = get_movement_logs(item_id=item.id)

                context.update({
                    'item': item,
                    'item_form': form,
                    'search_form': False,
                    'bin_warehouse_matrix': bin_warehouse_matrix,
                    'movement_logs': movement_logs,
                })
            except Item.DoesNotExist:
                messages.error(request, f"No item found with SKU '{search_sku}'")

        context['bins'] = Bin.objects.all().order_by('bin_name')
        context['movement_types'] = MovementType.objects.all().order_by('code')

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        sku = request.POST.get("SKU")

        if not sku:
            messages.error(request, "SKU is required.")
            return redirect(reverse("problem-solve-page"))
        try:
            item = Item.objects.get(SKU__iexact=sku)
            form = ItemForm(request.POST, instance=item)


            if form.is_valid():
                updated_item = form.save()
                messages.success(request, f"Item '{updated_item.item_name}' (SKU: {updated_item.SKU}) successfully updated.")

                if updated_item != sku:
                    return redirect(f"{request.path}?search_sku={updated_item.SKU}")

                form = ItemForm(instance=updated_item)
                return render(request, self.template_name, {
                    'item': updated_item,
                    'item_form': form,
                    'search_form': False
                })
            else:
                # If form validation failed, show the form with errors
                return render(request, self.template_name, {
                    'search_form': True,
                    'item': item,
                    'form': form,
                    'search_sku': sku
                })

        except Item.DoesNotExist:
            messages.error(request, f"Item with SKU '{sku}' no longer exists.")
            return redirect('problem_solve')
