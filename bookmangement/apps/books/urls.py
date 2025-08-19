from django.urls import path
from .views import BookManagement,ListUploaderBook

urlpatterns = [
    path('books/', BookManagement.as_view(), name='books'),
    path('books/<int:id>/', BookManagement.as_view(), name='book-detail'),  
    path('my-books/', ListUploaderBook.as_view(), name='my-books'),
]
