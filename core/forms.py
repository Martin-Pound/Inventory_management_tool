from django import forms
from .models import Bin, Warehouse, Supplier, Category

class BinForm(forms.ModelForm):
    class meta:
        model = Bin
        fields = ['bin_name', 'warehouse_name',]
        labels = {
            'bin_name': 'Bin Name',
            'warehouse_name': 'Warehouse Name',
        }
        error_messages = {
            'bin_name': {
                'required': 'Bin name is required',
                'max_length': 'Please enter a shorter bin name'
            },
            'warehouse_name': {
                'required': 'Warehouse name is required',
            }
        }