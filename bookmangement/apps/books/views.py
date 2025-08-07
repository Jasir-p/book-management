from django.shortcuts import render
from rest_framework.views import APIView
from .models import Books
from .serializers import BooksSerializer,BooksViewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import Is_Uploader
from .services import get_all_books,get_my_books,get_book_by_id,delete_book,create_book
# Create your views here.

class BookManagement(APIView):
    
    def get_permissions(self):
        if self.request.method in ['POST','GET']:
            return [IsAuthenticated()]
        return [IsAuthenticated(),Is_Uploader()]

    def get(self, request):
        # Retrieve all books from the database
        books = get_all_books()
        serializer = BooksViewSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Create a new book in the database
        serializer = BooksSerializer(data=request.data)
        if serializer.is_valid():
            create_book(request, serializer.validated_data)
            return Response({"message:Successfully added"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    

    def delete (self, request, *args, **kwargs):
        # Delete a book from the database
        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Book Id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        book = get_book_by_id(book_id)
        if not book:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,book)
        book.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_200_OK)


