from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import ReplySerializer
from .models import Reply

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    
    def get_serializer_class(self):
        return ReplySerializer

    @action(detail=False, methods=['post'])
    def create_reply(self, request):
        serializer = ReplySerializer(data=request.data)
        if serializer.is_valid():
            try:
                reply = serializer.save()
                return Response(
                    {
                        "message": "Reply added successfully",
                        "review": reply.review.id,
                        "seller": reply.seller.email,
                        "content": reply.content
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def get_replies(self, request, pk=None):
        # pk is the review ID
        replies = Reply.objects.filter(review=pk)
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)