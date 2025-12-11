from rest_framework import serializers
from core.models import MovementLog, Item, Bin, Warehouse, MovementType

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

    class Meta:
        model = MovementLog
        fields = ['id', 'item', 'from_bin', 'to_bin', 'quantity', 'movement_type', 'date_moved']