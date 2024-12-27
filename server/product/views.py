from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Product
from .serializers import ProductSerializer, ProductAddSerializer, ProductRemoveSerializer
from review.models import Review

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action == 'add_product':
            return ProductAddSerializer
        elif self.action == 'remove_product':
            return ProductRemoveSerializer
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
    
    @action(detail=False, methods=['post'])
    def remove_product(self, request):
        serializer = ProductRemoveSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = Product.objects.get(name=serializer.validated_data['name'], seller=serializer.validated_data['seller'])
                product.delete()
                return Response(
                    {
                        "message": "Product removed successfully",
                        "seller": product.seller.username,
                        "name": product.name
                    },
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def get_rating(self, request, pk=None):
        reviews = Review.objects.filter(product=pk)
        products = Product.objects.get(id=pk)

        if not products:
            return Response(
                {
                    "error": "Product not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if reviews.exists():
            rating = 0
            for review in reviews:
                rating += review.rating
            rating = rating / reviews.count()
        else:
            rating = 0.0

        return Response(
            {
                "rating": rating
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'])
    def get_products(self, request, pk=None):
        product = Product.objects.filter(seller=pk)
        serializer = ProductSerializer(product, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)