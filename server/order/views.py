from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import *
from product.models import Product
from account.models import Account
from orderdetail.models import OrderDetail
from orderdetail.views import OrderDetailViewSet

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if (self.action == 'create'):
            return CreateOrderSerializer
        elif (self.action == 'update_status'):
            return UpdateOrderSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['post'])
    def create(self, request):
        buyer_id = request.data.get('buyer')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        
        if not buyer_id or not product_id or quantity is None:
            return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            buyer = Account.objects.get(id = buyer_id)
            if (buyer.role != 'CUSTOMER'):
                return Response({
                    "error": "Only customers can create orders"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            order = Order.objects.create(buyer = buyer, total_price = 0, status = 'PENDING')
            # serializer = OrderSerializer(data=order)
        except:
            return Response({
                "error": "Something sus happened"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        queue = []
        
        try:
            print(product_id)
            for i in range(len(product_id)):
                print('Get product')
                product = Product.objects.get(id = product_id[i])
                print('Check quantity')
                if (product.quantity_in_stock < quantity[i]):
                    order.delete()
                    return Response({"error": "Quantity does not sufficient"}, status=status.HTTP_400_BAD_REQUEST)
                queue.append({"quantity": quantity[i], "order": order.id, "product": product_id[i]})
            print('Order detail')
            OrderDetailViewSet.backend_create_orderdetails(data=queue)
            print('Done')
        except:
            order.delete()
            return Response({"error": "Something has happened"}, status=status.HTTP_400_BAD_REQUEST)
            
        # Create orders with order details
        
        # Order details
        # if (serializer.is_valid()):
        return Response({"message": "Order successfully"}, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def update_status(self, request):
        account_id = request.data.get('account')
        order_id = request.data.get('order')
        new_status = request.data.get('status')
        print(account_id, order_id, new_status)
        try:
            account = Account.objects.get(id = account_id)
            order = Order.objects.get(id = order_id)
            if (account.role == 'CUSTOMER' and new_status == 'CANCELLED' and order.status != 'DELIVERED'):
                order.status = 'CANCELLED'
                order.save()
                return Response({"message": "Cancel successfully"}, status=status.HTTP_200_OK)
            elif (account.role == 'CUSTOMER' and new_status == 'DELIVERED' and order.status == 'SHIPPED'):
                order.status = 'DELIVERED'
                order.save()
                return Response({"message": "Deliver successfully"}, status=status.HTTP_200_OK)
            elif (account.role == 'SELLER' and new_status == 'PROCESSING' and order.status == 'PENDING'):
                order.status = 'PROCESSING'
                order.save()
                return Response({"message": "Order is in process"}, status=status.HTTP_200_OK)
            elif (account.role == 'SELLER' and new_status == 'SHIPPED' and order.status == 'PROCESSING'):
                order.status = 'SHIPPED'
                order.save()
                return Response({"message": "Order is being delivered"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Something happened"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Account or Order does not exist"})