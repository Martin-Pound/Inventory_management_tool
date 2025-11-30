from django.db import models

# Create your models here.

#Category model
class Category(models.Model):
    category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name

#Supplier model
class Supplier(models.Model):
    supplier_name = models.CharField(max_length=100)
    contact_email = models.EmailField()

    class Meta:
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.supplier_name

#Warehouse model
class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=50)
    street_address = models.CharField(max_length=120)
    postcode = models.CharField(max_length=8)

    class Meta:
        verbose_name_plural = "Warehouses"

    def __str__(self):
        return self.warehouse_name

#Bin model
class Bin(models.Model):
    bin_name = models.CharField(max_length=50)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name="bins")

    class Meta:
        verbose_name_plural = "Bins"

    def __str__(self):
        return f"{self.bin_name} - {self.warehouse.warehouse_name}"

#Item model
class Item(models.Model):
    item_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    SKU = models.CharField(max_length=50, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="items")
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, related_name="items")

    class Meta:
        verbose_name_plural = "Items"

    def __str__(self):
        return self.item_name

#Stock level
class StockLevel(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="stock_levels")
    bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name="stock_levels")
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("item", "bin")
        verbose_name_plural = "Stock Levels"

    def __str__(self):
        return f"{self.item.item_name} - {self.bin.bin_name} units"

#Movement types
class MovementType(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name_plural = "Movement Types"

    def __str__(self):
        return f"{self.code} - {self.name}"

#Movement log
class MovementLog(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    from_bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name="movements_from")
    to_bin = models.ForeignKey(Bin, on_delete=models.CASCADE, related_name="movements_to")
    quantity = models.PositiveIntegerField()
    date_moved = models.DateTimeField(auto_now_add=True)
    movement_type = models.ForeignKey(MovementType, on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name_plural = "Movement Logs"

    def __str__(self):
        return f"Moved {self.quantity} of {self.item.item_name} from {self.from_bin.bin_name} to {self.to_bin.bin_name} on {self.date_moved}"
