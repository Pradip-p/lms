from rest_framework import serializers
from .models import CustomUser, Book, BookDetails, BorrowedBooks

class CreateCustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        
    def validate_email(self, value):
        """
        Validate that the email address is unique and follows a valid format.
        """
        existing_users = CustomUser.objects.filter(email=value)
        if self.instance:
            existing_users = existing_users.exclude(pk=self.instance.pk)  # Exclude the current instance for updates

        if existing_users.exists():
            raise serializers.ValidationError("Email address must be unique.")
        return value
    
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['userID','name','email','membership_date']
        
    def validate_email(self, value):
        """
        Validate that the email address is unique and follows a valid format.
        """
        existing_users = CustomUser.objects.filter(email=value)
        if self.instance:
            existing_users = existing_users.exclude(pk=self.instance.pk)  # Exclude the current instance for updates

        if existing_users.exists():
            raise serializers.ValidationError("Email address must be unique.")
        return value

class BookDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDetails
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_isbn(self, value):
        """
        Validate that the ISBN is unique and has a length less than 10.
        """
        if len(value) >= 10:
            raise serializers.ValidationError("ISBN length must be less than 10 characters.")

        existing_books = Book.objects.filter(isbn=value)
        if self.instance:
            existing_books = existing_books.exclude(pk=self.instance.pk)  # Exclude the current instance for updates

        if existing_books.exists():
            raise serializers.ValidationError("ISBN must be unique.")

        return value



class BorrowedBooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowedBooks
        fields = '__all__'
