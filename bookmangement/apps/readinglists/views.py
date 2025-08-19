from django.shortcuts import render
from rest_framework import views,status,permissions,generics
from rest_framework.response import Response
from .models import ReadingList,ReadingListBook
from .serializers import ReadingListBookSerializer,ReadingListSerializer,ReadingListBookViewSerializer,ReadingListWithBooksSerializer
from .services import (
    get_reading_list,
   get_all_reading_list,books_with_order_list,add_book_reading_list,remove_book_reading_list,book_with_list,update_order_reading_list)
from .permissions import IsListOwner
from django.shortcuts import get_object_or_404
from bookmangement.paginations import StandardResultsSetPagination



class ReadingListView(views.APIView):
    
    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsListOwner(), permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    
    def get(self, request,pk=None):
        if pk:
            reading_list = get_reading_list(pk)
            serializer = ReadingListSerializer(reading_list)
            return Response(serializer.data)
        else:
            reading_list = get_all_reading_list(request)
            serializer = ReadingListSerializer(reading_list, many=True)
            return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = ReadingListSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            reading_list = get_reading_list(pk)
            self.check_object_permissions(request, reading_list)
            serializer = ReadingListSerializer(reading_list, data=request.data,context={'request': request}, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error":str(e)},status=status.HTTP_400_BAD_REQUEST)
    
    def delete( self, request, pk):
        try:
            reading_list = get_reading_list(pk)
            self.check_object_permissions(request, reading_list)
            reading_list.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ReadingListBookManagement(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsListOwner]
    def post (self, request):
        try:
            reading_list_id = request.data.get('reading_list')
            if not reading_list_id:
                return Response({"error": "reading_list_id is required"}, status=status.HTTP_400_BAD_REQUEST
                )
            reading_list = get_reading_list(reading_list_id)

            #check permission whether user is owner of reading list
            self.check_object_permissions(request, reading_list)

            serializer = ReadingListBookSerializer(data=request.data)
            if serializer.is_valid():
                print(serializer.validated_data['book'])
                add_book_reading_list(reading_list_id,serializer.validated_data['book'])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:

            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def patch( self, request):
        try:
            reading_list_with_book_id = request.data.get('reading_list_book')
            
            if not reading_list_with_book_id:
                return Response({"error": "reading_list_id is required"}, status=status.HTTP_400_BAD_REQUEST
                                )
            new_order = request.data.get('order')
            if  not new_order:
                return Response({"error": "order is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            list_book = book_with_list(reading_list_with_book_id)
            reading_list =get_reading_list(list_book.reading_list.id)
            self.check_object_permissions(request,reading_list )
            result = update_order_reading_list(list_book, new_order)

            if not result:
                return Response({"error": "Invalid order"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"message": "Order updated successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(str(e))
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
            
            reading_list_id = request.data.get('reading_list')
            book_id = request.data.get('book')
            if not reading_list_id:
                return Response({"error": "reading_list_id is required"}, status=status.HTTP_400_BAD_REQUEST
                                )
            if not book_id :
                return Response({"error": "book_id is required"}, status=status.HTTP_400_BAD_REQUEST
                            )
            reading_list = get_reading_list(reading_list_id)    
            self.check_object_permissions(request, reading_list)
            try:
                remove_book_reading_list(reading_list_id, book_id)
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Exception as e:
                print(str(e))
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            

class ListBookView(generics.ListAPIView):
    serializer_class = ReadingListWithBooksSerializer
    permission_classes = [permissions.IsAuthenticated, IsListOwner]

    def get_queryset(self):
        pk = self.kwargs.get("pk")
        reading_list = get_reading_list(pk)
        self.check_object_permissions(self.request, reading_list)
        return books_with_order_list(pk)


    


    

