from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import transaction
from core.models import Item, MovementLog, MovementType, Bin, StockLevel



def get_item_by_sku(sku):
    '''Helper function to get an item by SKU or raise a validation error.'''
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


def update_stock_level(item,
        bin,
        quantity_change):
    """Updates the stock level of an item in a specific bin."""
    stock_level, created = StockLevel.objects.get_or_create(item=item, bin=bin, defaults={'quantity': 0})
    stock_level.quantity += quantity_change

    # Prevent negative quantities
    if stock_level.quantity < 0:
        raise ValidationError(
            f"Cannot reduce stock below zero for {item.SKU} in bin {bin.bin_name} "
            f"(current: {stock_level.quantity - quantity_change}, change: {quantity_change})")

    stock_level.full_clean()
    stock_level.save()
    return stock_level


@transaction.atomic #Ensures an atomic database transaction
def log_movement(sku,
        from_bin_name,
        to_bin_name,
        quantity,
        movement_code):
    """
    Logs the movement of an item from one bin to another using the item's SKU.

    Args:
        sku: The Stock Keeping Unit of the item
        from_bin_name: Source bin name
        to_bin_name: Destination bin name
        quantity: Quantity being moved
        movement_code: Type of movement
    """
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
