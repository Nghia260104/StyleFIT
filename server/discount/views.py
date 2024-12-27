from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Discount
from .serializers import DiscountSerializer, DiscountCreateSerializer, DiscountEditSerializer, DiscountListSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()

    def get_serializer_class(self):
        if self.action == 'create_discount':
            return DiscountCreateSerializer
        elif self.action == 'edit_discount':
            return DiscountEditSerializer
        elif self.action == 'list_discounts':
            return DiscountListSerializer
        return DiscountSerializer

    @action(detail=False, methods=['post'])
    def create_discount(self, request):
        serializer = DiscountCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                discount = serializer.save()
                return Response(
                    {
                        "message": "Discount created successfully",
                        "seller": discount.seller.username,
                        "season": discount.season,
                        "year": discount.year,
                        "limit": discount.limit
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put'])
    def edit_discount(self, request, pk=None):
        try:
            discount = self.get_object()

            # Check permissions
            if request.user.id != discount.seller.id:
                return Response(
                    {"status": "error",
                     "message": "You don't have permission to edit this discount"
                    }, status=status.HTTP_403_FORBIDDEN)
            
            # Check if the user is a seller
            if request.user.role != 'SELLER':
                return Response({
                    "status": "error",
                    "message": "Only sellers can edit discounts"
                    },status=status.HTTP_403_FORBIDDEN)
            
            serializer = DiscountEditSerializer(discount, data=request.data, partial=True)
            if serializer.is_valid():
                # Check if discount should be deleted
                if serializer.validated_data.get('should_delete', False):
                    discount.delete()
                    return Response({
                        "status": "success",
                        "message": "Discount has been automatically deleted as it reached its limit"
                    }, status=status.HTTP_200_OK)
                

                updated_discount = serializer.save()
                return Response({
                    "status": "success",
                    "message": "Discount updated successfully",
                    "discount": {
                        "name": updated_discount.name, 
                        "description": updated_discount.description,
                        "percentage": updated_discount.percentage,
                        "season": updated_discount.season,
                        "product": updated_discount.product,
                        "category": updated_discount.category,
                        "limit": updated_discount.limit,
                        "used_number": updated_discount.used_number
                    }
                }, status=status.HTTP_200_OK)
            
            return Response({
                "status": "error",
                "message": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Discount.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Discount not found"
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def list_discounts(self, request):
        try:
            # Get filters from query params
            seller_id = request.query_params.get('seller')
            season = request.query_params.get('season')
            year = request.query_params.get('year')

            # Start with all discounts
            queryset = Discount.objects.all()

            # Apply filters
            if seller_id:
                queryset = queryset.filter(seller_id=seller_id)
            if season:
                queryset = queryset.filter(season=season)
            if year:
                queryset = queryset.filter(year=year)

            serializer = DiscountListSerializer(queryset, many=True)
            
            return Response({
                "status": "success",
                "count": len(serializer.data),
                "discounts": serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({
                "status": "error",
                "message": str(e)
            }, status=status.HTTP_400_BAD_REQUEST)