from django.core.exceptions import ValidationError, ObjectDoesNotExist
from core.models import Item, Supplier, Category

def create_item(item_name, description, SKU, category_name, supplier_name):
    """
    Creates a new inventory item with the provided details. Validates the uniqueness
    of the SKU before creation and ensures the existence of the category and
    supplier.
    """

    # Check for unique SKU
    if Item.objects.filter(SKU=SKU).exists():
        raise ValidationError(f"Item with SKU '{SKU}' already exists.")

    # Validate category and supplier existence
    try:
        category = Category.objects.get(category_name=category_name)
    except ObjectDoesNotExist:
        raise ValidationError(f"Category '{category_name}' does not exist.")

    try:
        supplier = Supplier.objects.get(supplier_name=supplier_name)
    except ObjectDoesNotExist:
        raise ValidationError(f"Supplier '{supplier_name}' does not exist.")

    item = Item(
        item_name=item_name,
        description=description,
        SKU=SKU,
        category=category,
        supplier=supplier
    )

    item.full_clean()  # Validate the model fields
    item.save()
    return item

