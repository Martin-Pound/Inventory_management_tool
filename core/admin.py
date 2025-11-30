from django.contrib import admin
from .models import (Category, Supplier, Warehouse, Bin, Item, StockLevel, MovementLog, MovementType)

# Register your models here.
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Warehouse)
admin.site.register(Bin)
admin.site.register(Item)
admin.site.register(StockLevel)
admin.site.register(MovementType)
admin.site.register(MovementLog)
