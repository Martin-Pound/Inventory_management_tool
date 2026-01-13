import random
from django.core.management.base import BaseCommand
from core.models import Category, Supplier, Warehouse, Bin, Item, StockLevel, MovementType


class Command(BaseCommand):
    help = "Seeds the database with initial data"

    def handle(self,
            *args,
            **kwargs):
        # Create Categories
        categories = ["Sports", "Furniture", "Stationery"]
        category_objs = [Category.objects.get_or_create(category_name=cat)[0] for cat in categories]

        # Create Suppliers
        suppliers = [("Tech Supplies Inc.", "tech@supplies.com"),
                     ("Home Goods Co.", "home@goods.com"),
                     ("Office Essentials Ltd.", "office@essentials.com")]
        supplier_objs = [Supplier.objects.get_or_create(supplier_name=name, contact_email=email)[0] for name, email in
                         suppliers]

        # Create Warehouses
        warehouses = [("Warehouse A", "123 Main St", "11111"),
                      ("Warehouse B", "456 Maple Ave", "22222")]
        warehouse_objs = [
            Warehouse.objects.get_or_create(warehouse_name=name, street_address=address, postcode=postcode)[0]
            for name, address, postcode in warehouses]

        #Create Receiving Bins
        for warehouse in warehouse_objs:
            receiving_bin_name = f"{warehouse.warehouse_name}-RECEIVING"
            Bin.objects.get_or_create(bin_name=receiving_bin_name, warehouse=warehouse)

        # Create Bins
        bin_objs = []
        for warehouse in warehouse_objs:
            for i in range(1, 11):  # 10 bins per warehouse
                bin_name = f"{warehouse.warehouse_name}-Bin{i:02d}"
                bin_objs.append(Bin.objects.get_or_create(bin_name=bin_name, warehouse=warehouse)[0])

        # Create Items
        items = [
            ("Laptop", "High-performance laptop", "SKU1", category_objs[0], supplier_objs[0]),
            ("Office Chair", "Ergonomic office chair", "SKU2", category_objs[1], supplier_objs[1]),
            ("Notepad", "100-page notepad", "SKU3", category_objs[2], supplier_objs[2]),
        ]
        item_objs = [
            Item.objects.get_or_create(item_name=name, description=desc, SKU=sku, category=cat, supplier=supplier)[0]
            for name, desc, sku, cat, supplier in items]

        # Create Movement Types
        movement_types = [("Stock In", "IN"), ("Stock Out", "OUT"), ("Transfer", "TR")]
        movement_type_objs = [MovementType.objects.get_or_create(name=name, code=code)[0] for name, code in
                              movement_types]

        # Create Stock Levels
        for item in item_objs:
            for bin_ in random.sample(bin_objs, 5):  # Randomly select 5 bins for each item
                quantity = random.randint(50, 200)  # Quantity between 50 and 200
                StockLevel.objects.get_or_create(item=item, bin=bin_, quantity=quantity)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully!"))
