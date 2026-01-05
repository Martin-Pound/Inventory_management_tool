from django.contrib import admin
from .models import (Category, Supplier, Warehouse, Bin, Item, StockLevel, MovementLog, MovementType)

class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "SKU", "supplier")  # Add at least one field to display
    search_fields = ("item_name", "SKU")  # Add search functionality


# Register your models here.
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Warehouse)
admin.site.register(Bin)
admin.site.register(Item, ItemAdmin)
admin.site.register(StockLevel)
admin.site.register(MovementType)
admin.site.register(MovementLog)
