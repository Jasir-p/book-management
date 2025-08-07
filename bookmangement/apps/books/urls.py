from django.urls import path
from .views import BookManagement

urlpatterns = [
    path('book-management/', BookManagement.as_view(), name='book-management'),
]
