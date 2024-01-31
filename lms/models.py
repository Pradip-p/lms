from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    """
    Custom manager for the CustomUser model.
    """
    def create_user(self, email, name, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        Create and return a superuser with administrative privileges.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with email-based login.
    """
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    membership_date = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """
        Return a string representation of the user, which is their email address.
        """
        return self.email



class Book(models.Model):
    """
    Represents a book in the library.

    Attributes:
    - bookID: Auto-incremented primary key for the book.
    - title: Title of the book.
    - isbn: ISBN (International Standard Book Number) of the book, unique.
    - published_date: Date when the book was published.
    - genre: Genre of the book.
    """
    bookID = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()
    genre = models.CharField(max_length=100)


class BookDetails(models.Model):
    """
    Represents additional details about a book.

    Attributes:
    - detailsID: Auto-incremented primary key for the details.
    - BookID: One-to-one relationship with a Book.
    - number_of_pages: Number of pages in the book.
    - publisher: Publisher of the book.
    - language: Language in which the book is written.
    """
    detailsID = models.AutoField(primary_key=True)
    bookID = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='details')
    number_of_pages = models.PositiveIntegerField()
    publisher = models.CharField(max_length=255)
    language = models.CharField(max_length=50)

class BorrowedBooks(models.Model):
    """
    Represents a record of a book being borrowed by a CustomUser.

    Attributes:
    - userID: Foreign key referring to the CustomUser who borrowed the book.
    - BookID: Foreign key referring to the Book that was borrowed.
    - borrow_date: Date when the book was borrowed.
    - return_date: Date when the book is returned. Nullable for ongoing borrowings.
    """
    userID = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='borrowed_books')
    bookID = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='borrowed_books')
    borrow_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
