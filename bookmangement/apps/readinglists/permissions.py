from rest_framework.permissions import BasePermission

class IsListOwner(BasePermission):
    """
    Custom permission to only allow owners upadte thier own lists.
    """
    def has_object_permission(self, request, view, obj):
        
        return obj.user == request.user

