from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from core.models import Item, MovementLog, MovementType, Bin, StockLevel, Warehouse


def warehouse_check(warehouse_name):
    #helper function to validate warehouse existence
    try:
        return Warehouse.objects.get(warehouse_name=warehouse_name)
    except ObjectDoesNotExist:
        raise ValidationError(f"Warehouse '{warehouse_name}' does not exist.")

def get_item_by_sku(sku):
    # Helper function to get an item by SKU
    try:
        return Item.objects.get(SKU=sku)
    except ObjectDoesNotExist:
        raise ValidationError(f"Item with SKU '{sku}' does not exist.")

def get_bin(bin_name):
    """Helper function to get a bin by name or create a virtual one for EXTERNAL."""
    try:
        return Bin.objects.get(bin_name=bin_name)
    except ObjectDoesNotExist:
        raise ValidationError(f"Bin '{bin_name}' does not exist.")

@transaction.atomic
def update_stock_level(item, bin, quantity_change):
    # Updates the stock level for a given item in a specific bin.
    stock_level, created = StockLevel.objects.get_or_create(item=item, bin=bin, defaults={'quantity': 0})
    stock_level.quantity += quantity_change

    # Prevent negative quantities
    if stock_level.quantity < 0:
        raise ValidationError(
            f"Cannot reduce stock below zero for {item.SKU} in bin {bin.bin_name} "
            f"(current: {stock_level.quantity - quantity_change}, change: {quantity_change})")

    elif stock_level.quantity == 0:
        stock_level.delete()
        return None

    stock_level.full_clean()
    stock_level.save()
    return stock_level

@transaction.atomic
def log_movement(sku, from_bin_name, to_bin_name, quantity, movement_code):
    # Logs a stock movement from one bin to another with the specified quantity and movement type.

    # Validate quantity
    if quantity <= 0:
        raise ValidationError("Movement quantity must be positive")

    # Get item by SKU
    item = get_item_by_sku(sku)

    # Get bins
    from_bin = get_bin(from_bin_name)
    to_bin = get_bin(to_bin_name)

    # Validate movement type
    try:
        movement_type = MovementType.objects.get(code=movement_code)
    except ObjectDoesNotExist:
        raise ValidationError(f"Movement type with code '{movement_code}' does not exist.")

    # Create movement log
    movement_log = MovementLog(
        item=item,
        from_bin=from_bin,
        to_bin=to_bin,
        quantity=quantity,
        movement_type=movement_type
    )
    movement_log.full_clean()
    movement_log.save()

    # Update stock levels
    update_stock_level(item, from_bin, -quantity)
    update_stock_level(item, to_bin, quantity)

    return movement_log

@transaction.atomic
def inbound_stock(item, warehouse, quantity):
    #Creates inbound stock movement to relevant warehouse's receiving bin

    #validate stock existence
    item = get_item_by_sku(item)
    #validate warehouse existence
    warehouse = warehouse_check(warehouse)
    #determine receiving bin name
    receiving_bin_name = f"{warehouse}_INBOUND"
    # get the bin object
    bin_obj = get_bin(receiving_bin_name)
    # updates stock level
    stock_level = update_stock_level(item, bin_obj, quantity)

    return stock_level




