from django.db import models
from apps.users.models import CustomeUser
# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Books(models.Model):
    title = models.CharField(max_length=110)
    author = models.ManyToManyField(Author, related_name="author")
    genre = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='books/image', null=True)
    description = models.TextField()
    upload_by = models.ForeignKey(CustomeUser, on_delete=models.CASCADE, related_name="upload_by", null=True)
    publication_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-publication_date']
        constraints = [
            models.UniqueConstraint(fields=['upload_by', 'title'], name='unique_book_per_user')
            ]
        

