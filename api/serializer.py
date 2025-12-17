from rest_framework import serializers
from core.models import MovementLog, Item, Bin, Warehouse, MovementType, StockLevel


class ItemSerializer(serializers.ModelSerializer):
    supplier = serializers.SlugRelatedField(
        queryset=Item.objects.all(),
        slug_field='supplier_name'
    )
    category = serializers.SlugRelatedField(
        queryset=Item.objects.all(),
        slug_field='category_name'
    )

    class Meta:
        model = Item
        fields = ['id', 'item_name', 'description', 'SKU', 'category', 'supplier']

class MovementLogSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(
        queryset=Item.objects.all(),
        slug_field='SKU'
    )
    from_bin = serializers.SlugRelatedField(
        queryset=Bin.objects.all(),
        slug_field='bin_name'
    )
    to_bin = serializers.SlugRelatedField(
        queryset=Bin.objects.all(),
        slug_field='bin_name'
    )
    movement_type = serializers.SlugRelatedField(
        queryset=MovementType.objects.all(),
        slug_field='code'
    )

    def validate_quantity(self, value):
        if not isinstance(value,int):
            raise serializers.ValidationError("Quantity must be an integer.")
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def validate(self, data):
        if not all([data.get('item'), data.get('from_bin'), data.get('to_bin'), data.get('movement_type'), data.get('quantity')]):
            raise serializers.ValidationError("Item, from_bin, to_bin, quantity, and movement_type are required fields.")
        return data

    class Meta:
        model = MovementLog
        fields = ['id', 'item', 'from_bin', 'to_bin', 'quantity', 'movement_type', 'date_moved']

class InboundMovementSerializer(serializers.ModelSerializer):
    item = serializers.SlugRelatedField(
        queryset=Item.objects.all(),
        slug_field='SKU'
    )
    warehouse = serializers.SlugRelatedField(
        queryset=Warehouse.objects.all(),
        slug_field='warehouse_name'
    )

    def validate_quantity(self, value):
        if not isinstance(value,int):
            raise serializers.ValidationError("Quantity must be an integer.")
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def validate(self, data):
        if not all([data.get('item'), data.get('warehouse'), data.get('quantity')]):
            raise serializers.ValidationError("Item, warehouse, and quantity are required fields.")
        return data

    class Meta:
        model = StockLevel
        fields = ['id', 'item', 'warehouse', 'quantity', 'updated']

