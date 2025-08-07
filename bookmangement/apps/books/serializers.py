from rest_framework import serializers
from .models import Books,Author
from utils.constants import FORBIDDEN_TITLE_CHARS_REGEX
import re
from PIL import Image

class BooksSerializer(serializers.ModelSerializer):
    authors_name = serializers.ListField(child=serializers.CharField(),write_only=True)

    class Meta:
        model = Books
        fields = fields = ['id', 'title', 'genre', 'description', 'authors_name']

    def validate_title (self, value):
        if len(value)<3:
            raise serializers.ValidationError('Title must be at least 3 characters long')
        
        if re.search(FORBIDDEN_TITLE_CHARS_REGEX,value):
            raise serializers.ValidationError("Title contains invalid characters:"
                                " /, -, _ are not allowed.")
        
        return value    
        

    def validate_genre(self, value):
        check = value.strip()
        if not check:
            raise serializers.ValidationError('Genre must be needed')
        if re.search(FORBIDDEN_TITLE_CHARS_REGEX, check):
            raise serializers.ValidationError("Genre contains invalid characters:"
                                              " /, -, _ are not allowed.")
        return value
    
    def cover_image(self, value):

        if value:
            try:
                img = Image.open(value)
                img.verify()
            except:
                raise serializers.ValidationError('Invalid image format')
            
        return value
    
class BooksViewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Books
        fields = ['id', 'title', 'genre', 'description', 'cover_image', 'author']

    def get_author(self, obj):
        return obj.author.values_list('name', flat=True)

        
    

