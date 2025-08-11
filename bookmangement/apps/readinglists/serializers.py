from rest_framework import serializers
from .models import ReadingList,ReadingListBook
from apps.books.serializers import BooksViewSerializer
from utils.constants import NAME_REGEX
import re

class ReadingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingList
        fields = ['id', 'name', 'description']

    def validate(self, attrs):
        name = attrs.get('name')
        print(name)
        if not re.match(NAME_REGEX,name):
            raise serializers.ValidationError('Invalid name')
        
        reading_list_id = self.instance.id if self.instance else None
        if ReadingList.objects.filter(name__iexact=name,user=self.context['request'].user).exclude(id=reading_list_id).exists():
            raise serializers.ValidationError({'name': 'ReadingList already exists'})

        return attrs
    
    def create (self, validated_data):
        return ReadingList.objects.create(**validated_data, user =self.context['request'].user)
    

class ReadingListBookSerializer(serializers.ModelSerializer):
    book = serializers.IntegerField()
    reading_list= serializers.IntegerField()

    class Meta:
        model = ReadingListBook
        fields = ['id', 'reading_list', 'book']

    def validate(self, attrs):
        if not self.instance:
            reading_list = attrs.get('reading_list')
            book = attrs.get('book')

            if not reading_list:
                raise serializers.ValidationError('Reading list is required')
            if not book:
                raise serializers.ValidationError('Book is required')
            
            if ReadingListBook.objects.filter(reading_list=reading_list, book=book).exists():
                raise serializers.ValidationError('Book is already in the reading list')
            
            
        return attrs
    
    
class ReadingListBookViewSerializer(serializers.ModelSerializer):
    book = BooksViewSerializer(read_only=True)
    class Meta:
        model = ReadingListBook
        fields = ['book','order','id']

    

class ReadingListWithBooksSerializer(serializers.ModelSerializer):
    reading_list_book = ReadingListBookViewSerializer(many=True)

    class Meta:
        model = ReadingList
        fields = ["id", "name", "description", "reading_list_book"]

    
    
    


