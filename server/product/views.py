from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product
from .serializers import ProductSerializer, ProductAddSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'add_product':
            return ProductAddSerializer
        return ProductSerializer

    @action(detail=False, methods=['post'])
    def add_product(self, request):
        serializer = ProductAddSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = serializer.save()
                return Response(
                    {
                        "message": "Product added successfully",
                        "seller": product.seller.username,
                        "name": product.name,
                        "quantity_in_stock": product.quantity_in_stock,
                        "price": product.price
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)