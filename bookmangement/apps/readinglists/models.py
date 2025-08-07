from users.models import CustomeUser
from books.models import Books
from django.db import models

# Create your views here.
class ReadingList(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ReadingListBook(models.Model):
    reading_list = models.ForeignKey(ReadingList, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




    
