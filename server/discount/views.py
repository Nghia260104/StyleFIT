from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Discount
from .serializers import DiscountSerializer, DiscountCreateSerializer

class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()

    @action(detail=False, methods=['post'])
    def create_discount(self, request):
        serializer = DiscountCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                discount = serializer.save()
                return Response(
                    {
                        "message": "Discount created successfully",
                        "seller": discount.seller,
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
    

# Create your views here.
