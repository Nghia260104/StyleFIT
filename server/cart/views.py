# from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Cart
from .serializers import *
from account.models import Account
from product.models import Product

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'get_cart':
            return GetCartSerializer
        elif self.action == 'update' or self.action == 'add':
            return HandleCartSerializer
        return CartSerializer
    
    @action(detail=False, methods=['post'])
    def update(self, request):
        buyer_id = request.data.get('buyer')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        
        if not buyer_id or not product_id or quantity is None:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            buyer = Account.objects.get(id = buyer_id)
            product = Product.objects.get(id = product_id)
            cart_item = Cart.objects.get(buyer = buyer, product = product)
        except:
            return Response({"error": "Something has happened"}, status=status.HTTP_400_BAD_REQUEST)
        
        if quantity <= 0:
            cart_item.delete()
            return Response({"delete": "Cart item deleted"}, status=status.HTTP_200_OK)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        return Response({"message": "Add to cart successfully"}, status = status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        buyer_id = request.data.get('buyer')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        
        if not buyer_id or not product_id or quantity is None:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            buyer = Account.objects.get(id = buyer_id)
            product = Product.objects.get(id = product_id)
        except:
            return Response({"error": "Something has happened"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = Cart.objects.get(buyer = buyer, product = product)
            cart_item.quantity = cart_item.quantity + quantity
            cart_item.save()
        except:
            Cart.objects.create(buyer = buyer, product = product, quantity = quantity)
        
        return Response({"message": "Add to cart successfully"}, status = status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def get_cart(self, request):
        buyer_id = request.query_params.get('buyer', None)
        
        filter = Q()
        if (buyer_id):
            filter &= Q(buyer=buyer_id)
        
        mydata = Cart.objects.all().filter(filter)
        
        serializer = CartSerializer(mydata, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    