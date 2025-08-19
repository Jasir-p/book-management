from .models import ReadingList,ReadingListBook
from django.shortcuts import get_object_or_404
from apps.books.models import Books
from django.db.models import F,Prefetch
from django.db import transaction


'''
This is for get the all reading list of user
'''
def get_all_reading_list(request):
    reading_list = ReadingList.objects.filter(user=request.user)
    return reading_list


def get_reading_list(pk):
    return get_object_or_404(ReadingList, pk=pk)
    

def  books_with_order_list(pk):
    reading_list_with_book = ReadingList.objects.filter(pk=pk).prefetch_related(
        Prefetch(
            "reading_list_book",
            queryset=ReadingListBook.objects.select_related("book").order_by("order"),

        )
    )
    return reading_list_with_book

def book_with_list(pk):
    reading_list_with_book = ReadingListBook.objects.get(id=pk)
    return reading_list_with_book


@transaction.atomic
def add_book_reading_list(reading_list_id,book_id,):
    print(book_id)
    book = get_object_or_404(Books, pk=book_id)
    reading_list = get_object_or_404(ReadingList, pk=reading_list_id)

    reading_list_books = ReadingListBook.objects.filter(reading_list=reading_list).update(order=F("order")+1)

    reading_list_book = ReadingListBook.objects.create(reading_list=reading_list, book=book, order=1)

    return reading_list_book

def remove_book_reading_list(reading_list_id,book_id,):
    reading_list_book = get_object_or_404(ReadingListBook,book__id=book_id, reading_list__id=reading_list_id)
    order= reading_list_book.order
    reading_list_book.delete()

    reading_list_books = ReadingListBook.objects.filter(reading_list__id=reading_list_id, 
                                                       order__gt=order).update(order=F("order")-1)
    

@transaction.atomic   
def update_order_reading_list(reading_list_book,order):
    reading_list_books_count = ReadingListBook.objects.filter(reading_list=reading_list_book.reading_list).count()
    print(reading_list_books_count)
    print(order)
    if order > reading_list_books_count or order<1:
        return False


    if order == reading_list_book.order:
        return reading_list_book
    
    original_order = reading_list_book.order
    
    if order < original_order:
        print('if')
        update_list=ReadingListBook.objects.filter(reading_list=reading_list_book.reading_list,
                        order__gte=order,order__lt=original_order)
        print(update_list)
        update_list.update(order=F("order")+1)
    else:
        print('else')
        update_list=ReadingListBook.objects.filter(reading_list=reading_list_book.reading_list, 
                        order__lte=order,order__gt=original_order)
        print(update_list)
        update_list.update(order=F("order")-1)
        
    reading_list_book.order= order
    reading_list_book.save()

    return reading_list_book
        
    

    