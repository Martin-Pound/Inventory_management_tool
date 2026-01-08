from django.contrib import admin
from .models import (Category, Supplier, Warehouse, Bin, Item, StockLevel, MovementLog, MovementType)

class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "SKU", "supplier")  # Add at least one field to display
    search_fields = ("item_name", "SKU")  # Add search functionality

class MovementLogAdmin(admin.ModelAdmin):
    list_display = ("item", "movement_type", "quantity", "date_moved", "from_bin", "to_bin")
    list_filter = ("movement_type", "date_moved")
    search_fields = ("item__item_name", "item__SKU")

# Register your models here.
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Warehouse)
admin.site.register(Bin)
admin.site.register(Item, ItemAdmin)
admin.site.register(StockLevel)
admin.site.register(MovementType)
admin.site.register(MovementLog, MovementLogAdmin)
