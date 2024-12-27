from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from product.models import Product
from account.models import Account

class OrderViewSet(ViewSet):
    @action(detail=False, methods=['post'])
    def create(self, request):
        buyer_id = request.data.get('buyer')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        
        if not buyer_id or not product_id or quantity is None:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id = product_id)
        except:
            return Response({"error": "Product does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        finally:
            if product.quantity_in_stock < quantity:
                return Response({"error": "Requested quantity is too big"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create orders with order details
        Order.objects.create(buyer= buyer_id, total_price = 0, status = 'PENDING')
        
        # Order details
    
    @action(detail=False, methods=['post'])
    def update_status(self, request):
        account_id = request.data.get('account')
        order_id = request.data.get('order')
        new_status = request.data.get('status')
        try:
            account = Account.objects.get(id = account_id)
            order = Order.objects.get(id = order_id)
            if (account.role == 'CUSTOMER' and new_status == 'Cancelled' and order.status != 'DELIVERED'):
                order.status = 'CANCELLED'
                order.save()
                return Response({"message": "Cancel successfully"}, status=status.HTTP_200_OK)
            elif (account.role == 'CUSTOMER' and new_status == 'Delivered' and order.status == 'SHIPPED'):
                order.status = 'DELIVERED'
                order.save()
                return Response({"message": "Deliver successfully"}, status=status.HTTP_200_OK)
            elif (account.role == 'SELLER' and new_status == 'Processing' and order.status == 'PENDING'):
                order.status = 'PROCESSING'
                order.save()
                return Response({"message": "Order is in process"}, status=status.HTTP_200_OK)
            elif (account.role == 'SELLER' and new_status == 'Shipped' and order.status == 'PROCESSING'):
                order.status = 'SHIPPED'
                order.save()
                return Response({"message": "Order is being delivered"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Something happened"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Account or Order does not exist"})