# from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Cart
from .serializers import CartSerializer

class CartViewSet(ViewSet):
    def update(self, request):
        buyer_id = request.data.get('buyer')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        
        if not buyer_id or not product_id or quantity is None:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = Cart.objects.get(buyer = buyer_id, product = product_id)
        except:
            return Response({"error": "Cart item not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        if quantity <= 0:
            cart_item.delete()
            return Response({"delete": "Cart item deleted"}, status=status.HTTP_200_OK)
        
        cart_item.quantity = quantity
        cart_item.save()
        
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def add(self, request):
        buyer_id = request.data.get('buyer')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        
        if not buyer_id or not product_id or quantity is None:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            cart_item = Cart.objects.get(buyer = buyer_id, product = product_id)
        except:
            Cart.objects.create(buyer = buyer_id, product = product_id, quantity = quantity)
        
        cart_item.quantity = cart_item.quantity + quantity
        cart_item.save()
        
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status = status.HTTP_200_OK)
    