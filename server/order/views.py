from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from product.models import Product
from account.models import Account
from orderdetail.models import OrderDetail
from orderdetail.views import OrderDetailViewSet

class OrderViewSet(ViewSet):
    @action(detail=False, methods=['post'])
    def create(self, request):
        buyer_id = request.data.get('buyer')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        
        if not buyer_id or not product_id or quantity is None:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(buyer= buyer_id, total_price = 0, status = 'PENDING')
        serializer = OrderSerializer(data=order)
        
        queue = []
        
        try:
            for i in range(product_id):
                product = Product.objects.get(id = product_id)
                if (product.quantity_in_stock < quantity):
                    order.delete()
                    return Response({"error": "Quantity does not sufficient"}, status=status.HTTP_400_BAD_REQUEST)
                queue.append({"quantity": quantity, "order": order.id, "product": product_id})
                
            OrderDetailViewSet.backend_create_orderdetails(data=queue)
        except:
            order.delete()
            return Response({"error": "Something has happened"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create orders with order details
        
        # Order details
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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