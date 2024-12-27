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