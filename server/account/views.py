from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Account
from .serializers import AccountSerializer, RegistrationSerializer

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    # serializer_class = RegistrationSerializer
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return RegistrationSerializer
        return AccountSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                account = serializer.save()
                return Response(
                    {
                        "message": "Account created successfully",
                        "email": account.email,
                        "profile_name": account.profile_name,
                        "role": account.role
                    },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": str(e)},
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
