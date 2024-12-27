from rest_framework import viewsets, status
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Order
from .serializers import *
from product.models import Product
from account.models import Account
from discount.models import Discount
from orderdetail.models import OrderDetail
from orderdetail.views import OrderDetailViewSet
from django.db.models import Q

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    
    def get_serializer_class(self):
        if (self.action == 'create'):
            return CreateOrderSerializer
        elif (self.action == 'update_status'):
            return UpdateOrderSerializer
        elif (self.action == 'get_order'):
            return GetOrderSerializer
        return OrderSerializer
    
    @action(detail=False, methods=['post'])
    def create(self, request):
        buyer_id = request.data.get('buyer')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        discount_id = request.data.get('discount')
        
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
            discount = Discount.objects.get(id = discount_id)
            max_price = 0
            total_price = 0
            for i in range(len(product_id)):
                print('Get product')
                product = Product.objects.get(id = product_id[i])
                print('Check quantity')
                if (product.quantity_in_stock < quantity[i]):
                    order.delete()
                    return Response({"error": "Quantity does not sufficient"}, status=status.HTTP_400_BAD_REQUEST)
                
                if (product.id in discount.product or product.category in discount.category):
                    max_price = max(max_price, product.price)
                total_price += product.price
                queue.append({"quantity": quantity[i], "order": order.id, "product": product_id[i]})
            print('Order detail')
            OrderDetailViewSet.backend_create_orderdetails(data=queue)
            if (max_price > 0):
                max_price = int(discount.percentage * max_price / 100)
                total_price = total_price - max_price
                discount.used_number += 1
                if (discount.limit <= discount.used_number):
                    discount.delete()
                else:
                    discount.save()
            order.total_price = total_price
            order.save()
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
        
    @action(detail=False, methods=['get'])
    def get_order(self, request):
        buyer_id = request.query_params.get('buyer', None)
        order_status = request.query_params.get('status', None)
        order_id = request.query_params.get('order', None)
        sort = request.query_params.get('sort', None)
        seller_id = request.query_params.get('seller', None)
        
        if seller_id:
            orders = Order.objects.filter(orderdetail__product__seller_id=seller_id, orderdetail__product__seller__role='SELLER').distinct()
            serializer = OrderSerializer(orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        filter = Q()
        if buyer_id:
            filter &= Q(buyer=buyer_id)
        if order_status:
            filter &= Q(status=order_status)
        if order_id:
            filter &= Q(id = order_id)
        
        filtered_data = Order.objects.all().filter(filter)
        
        if sort == 'asc':
            filtered_data = filtered_data.order_by('create_at')
        elif sort == 'desc':
            filtered_data = filtered_data.order_by('-created_at')
            
        # print(filtered_data)
            
        serializer = OrderSerializer(filtered_data, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)