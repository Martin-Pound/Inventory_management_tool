from rest_framework import views, status
from rest_framework.response import Response
from core.services.inventory import create_item
from django.core.exceptions import ValidationError
from api.serializer import ItemSerializer, MovementLogSerializer
from core.services.inv_movements import log_movement

class CreateItemView(views.APIView):
    def post(self,
            request,
            format=None):
        try:
            # Extract required fields from request data
            item_name = request.data.get('item_name')
            description = request.data.get('description')
            SKU = request.data.get('SKU')
            category_name = request.data.get('category_name')
            supplier_name = request.data.get('supplier_name')

            # Validate required fields
            if not all([item_name, SKU, category_name, supplier_name]):
                return Response(
                    {"error": "Missing required fields"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Call the microservice function
            item = create_item(
                item_name=item_name,
                description=description,
                SKU=SKU,
                category_name=category_name,
                supplier_name=supplier_name
            )

            # Use the serializer to format the response
            serializer = ItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to create item: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class MovementLogView(views.APIView):
    def post(self,
            request,
            format=None):
        try:
            # Extract fields
            sku = request.data.get('sku')
            from_bin_name = request.data.get('from_bin_name')
            to_bin_name = request.data.get('to_bin_name')
            quantity = request.data.get('quantity')
            movement_code = request.data.get('movement_code')

            # Validate required fields
            if not all([sku, from_bin_name, to_bin_name, quantity, movement_code]):
                return Response(
                    {"error": "Missing required fields"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate quantity is an integer
            try:
                quantity = int(quantity)
            except (ValueError, TypeError):
                return Response(
                    {"error": "Quantity must be an integer"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Call service function
            movement_log = log_movement(
                sku=sku,
                from_bin_name=from_bin_name,
                to_bin_name=to_bin_name,
                quantity=quantity,
                movement_code=movement_code
            )

            serializer = MovementLogSerializer(movement_log)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"Failed to log movement: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
