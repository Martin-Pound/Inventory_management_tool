from rest_framework import views, status
from rest_framework.response import Response
from core.services.inventory import create_item
from django.core.exceptions import ValidationError
from api.serializer import ItemSerializer, MovementLogSerializer, InboundMovementSerializer
from core.services.inv_movements import log_movement
from core.services.inv_movements import inbound_stock

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

class InboundStockView(views.APIView):
    def post(self, request, format=None):
        # Implementation for inbound stock logging would go here
        try:
            serializer = InboundMovementSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data

                # Extract validated fields
                sku = validated_data['item'].SKU
                warehouse_name = validated_data['warehouse'].warehouse_name
                quantity = validated_data['quantity']

                # Call the service function to log the inbound movement
                inbound_stock_record = inbound_stock(
                    item=sku,
                    warehouse=warehouse_name,
                    quantity=quantity,
                )

                # Create a custom response dictionary with the fields we want
                response_data = {
                    "item": inbound_stock_record.item.SKU,
                    "warehouse": warehouse_name,  # Use the original warehouse name
                    "quantity": inbound_stock_record.quantity,
                    "bin": inbound_stock_record.bin.bin_name
                }

                # Serialize and return the response
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

class MovementLogView(views.APIView):
    def post(self, request, format=None):
        try:
            # Validate payload using MovementLogSerializer
            serializer = MovementLogSerializer(data=request.data)
            if serializer.is_valid():
                validated_data = serializer.validated_data

                # Extract validated fields
                sku = validated_data['item'].SKU
                from_bin_name = validated_data['from_bin'].bin_name
                to_bin_name = validated_data['to_bin'].bin_name
                quantity = validated_data['quantity']
                movement_code = validated_data['movement_type'].code

                # Call the service function to log the movement
                movement_log = log_movement(
                    sku=sku,
                    from_bin_name=from_bin_name,
                    to_bin_name=to_bin_name,
                    quantity=quantity,
                    movement_code=movement_code,
                )

                # Serialize and return the response
                response_serializer = MovementLogSerializer(movement_log)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            else:
                # Return serializer validation errors
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError as e:
            # Handle ValidationError from log_movement or serializer
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Catch any other server-side errors
            return Response(
                {"error": f"An unexpected error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

