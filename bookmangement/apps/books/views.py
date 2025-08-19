from django.shortcuts import render
from rest_framework import views,generics
from .models import Books
from .serializers import BooksSerializer,BooksViewSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import Is_Uploader
from .services import list_all_books,list_my_books,get_book_by_id,delete_book,create_book
from django.db import IntegrityError
from bookmangement.paginations import StandardResultsSetPagination,paginate_queryset_with_serializer
# Create your views here.

class BookManagement(views.APIView):
    
    def get_permissions(self):
        if self.request.method in ['POST','GET']:
            return [IsAuthenticated()]
        return [IsAuthenticated(),Is_Uploader()]

    def get(self, request,id=None):
        if id:
            book =get_book_by_id(id)
            serializer = BooksViewSerializer(book)
            return Response(serializer.data)

        else:
            # Retrieve all books from the database
            books = list_all_books()
            return paginate_queryset_with_serializer(books,request,BooksViewSerializer,page_size=5)

    def post(self, request, *args, **kwargs):
        # Create a new book in the database
        try:

            serializer = BooksSerializer(data=request.data)
            if serializer.is_valid():
                create_book(request, serializer.validated_data)
                return Response({"message:Successfully added"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except IntegrityError:
            return Response({"message": "Book already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch (self, request, id=None):
        if not id:
            return Response({'error': 'Book Id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        book = get_book_by_id(id)

        serializer = BooksSerializer(book,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book updated successfully", "book": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete (self, request, *args, **kwargs):
        # Delete a book 

        book_id = request.data.get('book_id')
        if not book_id:
            return Response({'error': 'Book Id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        book = get_book_by_id(book_id)
        if not book:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        self.check_object_permissions(request,book)
        book.delete()
        return Response({'message': 'Book deleted successfully'}, status=status.HTTP_200_OK)


class ListUploaderBook(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BooksViewSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):

        return list_my_books(self.request)
    





