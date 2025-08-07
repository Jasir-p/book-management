from django.urls import path
from .views import BookManagement,ListUploaderBook

urlpatterns = [
    path('book-management/', BookManagement.as_view(), name='book-management'),
    path('list-uploader-book/', ListUploaderBook.as_view(), name='list-uploader-book')
]
