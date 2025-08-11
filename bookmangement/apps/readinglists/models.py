from apps.users.models import CustomeUser
from apps.books.models import Books
from django.db import models

# Create your views here.
class ReadingList(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, related_name='reading_list')
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_reading_list')
            ]

class ReadingListBook(models.Model):
    reading_list = models.ForeignKey(ReadingList, on_delete=models.CASCADE, related_name="reading_list_book")
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    order = models.IntegerField()

    class Meta:
        ordering = ['order']
        constraints = [
            models.UniqueConstraint(fields=['reading_list', 'book'], name='unique_reading_list_book'),
            ]
        






    
