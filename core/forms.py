from django import forms
from .models import Bin, Warehouse, Supplier, Category, Item

class BinForm(forms.ModelForm):
    class Meta:
        model = Bin
        fields = ['bin_name', 'warehouse',]
        labels = {
            'bin_name': 'Bin Name',
            'warehouse': 'Warehouse Name',
        }

        def clean(self):
            cleaned_data = super().clena()
            bin_name = cleaned_data.get('bin_name')
            warehouse = cleaned_data.get('warehouse')

            if bin_name and warehouse:
                # Check if this bin name already exists in the warehouse
                if Bin.objects.filter(bin_name=bin_name, warehouse=warehouse).exists():
                    raise forms.ValidationError(
                        f"A bin named '{bin_name}' already exists in {warehouse.warehouse_name}."
                    )

            return cleaned_data


class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['warehouse_name', 'street_address', 'postcode']
        labels = {
            'warehouse_name': 'Warehouse Name',
            'street_address': 'Street Address',
            'postcode': 'Postcode',
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
        labels = {
            'category_name': 'Category Name',
        }
        error_messages = {
            'category_name': {
                'unique': "This category already exists. Please choose a different name.",
            },
        }

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'contact_email']
        labels = {
            'supplier_name': 'Supplier Name',
            'contact_email': 'Contact Email',
        }
        error_messages = {
            'supplier_name': {
                'unique': "This supplier already exists. Please choose a different name.",
            },
            'contact_email': {
                'unique': "This email is already associated with another supplier. Please use a different email.",
                'invalid': "Enter a valid email address.",
            },

        }

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['item_name', 'description', 'SKU', 'category', 'supplier']
        labels = {
            'item_name': 'Item Name',
            'description': 'Description',
            'SKU': 'SKU',
            'category': 'Category',
            'supplier': 'Supplier',
        }
        error_messages = {
            'SKU': {
                'unique': "This SKU already exists. Please choose a different SKU.",
            },
        }