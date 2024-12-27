from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import OrderDetail
from .serializers import OrderDetailSerializer
from product.models import Product
from order.models import Order
from django.db import transaction

class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.all()
    serializer_class = OrderDetailSerializer

    @action(detail=False, methods=['post'])
    def create_orderdetails(self, request):
        serializer = OrderDetailSerializer(data=request.data, many=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    orderdetails = serializer.save()  # Save all validated data
                return Response(
                    {
                        "message": "Order details created successfully",
                        "orderdetails": serializer.data,  # Return serialized data
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def backend_create_orderdetails(data):
        serializer = OrderDetailSerializer(data=data, many=True)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    orderdetails = serializer.save()  # Save all validated data
                return Response(
                    {
                        "message": "Order details created successfully",
                        "orderdetails": serializer.data,  # Return serialized data
                    },
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def get_orderdetails(self, request, pk=None):
        try:
            # Retrieve OrderDetail instances related to the specified order ID
            orderdetails = OrderDetail.objects.filter(order_id=pk)
            response_data = []

            for orderdetail in orderdetails:
                product = orderdetail.product  # This is already a Product object
                name = product.name  # Access the name directly
                price = product.price * orderdetail.quantity  # Compute total price

                response_data.append({
                    "id": product.id,  # Use the ID directly
                    "product": name,
                    "quantity": orderdetail.quantity,
                    "unitPrice": product.price,
                    "price": price,
                })

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
