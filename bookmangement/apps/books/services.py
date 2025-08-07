from .models import Books,Author
from django.core.exceptions import ObjectDoesNotExist


def get_all_books():
    return Books.objects.filter(is_active=True)

def get_my_books(request):
    return Books.objects.filter(user=request.user, is_active=True)

def get_book_by_id(book_id):
    try:
        return Books.objects.get(id=book_id)
    except Books.DoesNotExist:
        return None

def create_book(request,validated_data):
    authors_name = validated_data['authors_name',[]]
    book = Books.objects.create(**validated_data, upload_by=request.user)
    for name in authors_name:
        author ,created = Author.objects.get_or_create(name=name)
        book.author.add(author)

def delete_book(book):
    return book.delete()