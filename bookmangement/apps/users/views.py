from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,UserViewSerializer
import logging
from .models import CustomeUser 
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from .permissions import IsOwner




# Create your views here.


class UserManagementView(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.  
    """
    queryset = CustomeUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        if self.action == 'list':
            return [IsAdminUser()]
        return [IsAuthenticated(),IsOwner()]
    def get_serializer_class(self):
        if self.action == 'list':
            return UserViewSerializer
        return UserSerializer
        
    

    