from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ReviewSerializer
from .models import Review

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    
    def get_serializer_class(self):
        return ReviewSerializer

    def create_review(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            try:
                review = serializer.save()
                return Response(
                    {
                        "message": "Review added successfully",
                        "product": review.product.name,
                        "buyer": review.buyer.email,
                        "content": review.content,
                        "rating": review.rating
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)