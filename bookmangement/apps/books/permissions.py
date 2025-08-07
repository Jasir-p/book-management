from rest_framework.permissions import BasePermission

class Is_Uploader(BasePermission):
    """
    Its check if the user is the uploader of the Book.
    """
    def has_object_permission(self, request, view, obj):
        return obj.upload_by == request.user
