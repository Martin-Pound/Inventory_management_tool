from rest_framework import views, status
from rest_framework.response import Response
from core.services.inventory import create_item
from django.core.exceptions import ValidationError
from api.serializer import ItemSerializer  # Import the serializer


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
