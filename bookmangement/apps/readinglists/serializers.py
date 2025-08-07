from rest_framework import serializers
from .models import ReadingList,ReadingListBook
from books.serializers import BooksViewSerializer
from utils.constants import NAME_REGEX


class ReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ('id', 'name', 'description')

    def validate(self, attrs):
        name = attrs.get('name')
        if not NAME_REGEX.match(name):
            raise serializers.ValidationError('Invalid name')
        
        reading_list_id = self.instance.id if self.instance else None
        if ReadingList.objects.filter(name__iexact=name).exclude(id=reading_list_id).exists():
            raise serializers.ValidationError({'name': 'Name already exists'})

        return attrs
    

class ReadingListBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReadingListBook
        fields = ('id', 'reading_list', 'book')

    def validate(self, attrs):
        reading_list = attrs.get('reading_list')
        book = attrs.get('book')

        if not reading_list:
            raise serializers.ValidationError('Reading list is required')
        if not book:
            raise serializers.ValidationError('Book is required')
        
        if ReadingListBook.objects.filter(reading_list=reading_list, book=book).exists():
            raise serializers.ValidationError('Book is already in the reading list')
        
        return attrs


    
    
    


