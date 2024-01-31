from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser, Book, BookDetails, BorrowedBooks
from .serializers import CustomUserSerializer, BookSerializer, BookDetailsSerializer, BorrowedBooksSerializer, CreateCustomUserSerializer
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .pagination import CustomPagination
from rest_framework.exceptions import NotFound


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user(request):
    """
    Register a new user.

    POST /api/register/

    Request:
    {
        "name": "John Thapa",
        "email": "john@example.com",
        "password": "secure_password"
    }

    Response:
    201 Created
    {
        "UserID": 1,
        "name": "John Thapa",
        "email": "john@example.com",
        "membership_date": "2022-01-30",
        "token": "generated_token"
    }
    """
    data = request.data

    # Check if 'email' and 'password' keys are present in the request data
    if 'email' not in data or 'password' not in data or 'name' not in data:
        return Response({"error": "name, email and password are required in the request data."}, status=status.HTTP_400_BAD_REQUEST)

    # Hash the password
    data['password'] = make_password(data['password'])

    # Set default values for is_staff and is_superuser
    data['is_staff'] = True
    data['is_superuser'] = False

    # Serialize the data
    serializer = CreateCustomUserSerializer(data=data)
    if serializer.is_valid():
        # Save the user
        custom_user = serializer.save()

        # Create a token for the user
        token, created = Token.objects.get_or_create(user=custom_user)

        # Add the token to the response data
        response_data = {
            "userID": custom_user.userID,
            "name": custom_user.name,
            "email": custom_user.email,
            "membership_date": custom_user.membership_date,
            "token": token.key  # Include the token in the response
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):

    """
    Get a list of all CustomUsers.

    GET /api/CustomUsers/list/

    Response:
    [
        {
            "UserID": 1,
            "name": "John Thapa",
            "email": "john@example.com",
            "membership_date": "2022-01-30"
        },
        ...
    ]
    """
    
    try:
        custom_users = CustomUser.objects.all().order_by('-userID')
        if not custom_users.exists():
            raise NotFound("No users found.")
        
        # Apply pagination
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(custom_users, request)

        serializer = CustomUserSerializer(result_page, many=True)
        return paginator.get_paginated_response({"message": "users retrieved successfully.","data":serializer.data})
    
    except CustomUser.DoesNotExist:
        raise NotFound("CustomUser model not found")
    except Exception as e:
        return Response({"error": str(e)}, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, id):
    """
    Get details of a CustomUser by ID.

    GET /api/CustomUsers/<int:id>/

    Response:
    200 OK - User details retrieved successfully
    {
        "userID": 1,
        "name": "John Thapa",
        "email": "john@example.com",
        "membership_date": "2022-01-30"
    }
    """
    try:
        user = CustomUser.objects.get(userID=id)
    except CustomUser.DoesNotExist:
        return Response({"message": f"Sorry, the user with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(user)
    return Response({"message": "User details retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)




@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request, id):  # Change 'id' to 'userID'
    try:
        user = CustomUser.objects.get(userID=id)  # Change 'id' to 'userID'
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CustomUserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User updated successfully", "data": serializer.data})
    return Response({"error": "Invalid data provided", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, id):  #
    try:
        user = CustomUser.objects.get(userID=id) 
        user.delete()
        return Response({"message": f"User with ID {user.name} successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
    except CustomUser.DoesNotExist:
        return Response({"error": f"User with ID { id } not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



# Book views

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book(request):
    """
    Create a new book.

    POST /api/books/create/

    Request:
    {
        "title": "The Great Gatsby",
        "isbn": "9781234567890",
        "published_date": "2022-01-30",
        "genre": "Fiction"
    }

    Response:
    201 Created
    {
        "bookID": 1,
        "title": "The Great Gatsby",
        "isbn": "9781234567890",
        "published_date": "2022-01-30",
        "genre": "Fiction"
    }
    """
        
    required_fields = ["title", "isbn", "published_date", "genre"]

    # Check if all required fields are present in the request data
    if not all(field in request.data for field in required_fields):
        return Response(
            {"error": "Required fields are missing. Please provide 'title', 'isbn', 'published_date', 'genre'."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Validate request data
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # Save the book
            serializer.save()

            # Return successful response
            return Response({"message":"Book created successfully", "data":serializer.data}, status=status.HTTP_201_CREATED)
        else:
            # Return validation error response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        # Generic internal server error
        return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_books(request):
    """
    Get a list of all books.

    GET /api/books/list/

    Response:
    200 OK - List of books retrieved successfully
    [
        {
            "bookID": 1,
            "title": "The Great Gatsby",
            "isbn": "9781234567890",
            "published_date": "2022-01-30",
            "genre": "Fiction"
        },
        ...
    ]
    """
    books = Book.objects.all().order_by('-bookID')

    if not books.exists():
        return Response({"message": "No books found."}, status=status.HTTP_404_NOT_FOUND)

    # Apply pagination
    paginator = CustomPagination()
    result_page = paginator.paginate_queryset(books, request)
    serializer = BookSerializer(result_page, many=True)

    # Set the status code directly in the Response object
    return paginator.get_paginated_response({"message": "List of books retrieved successfully", "data": serializer.data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book_by_id(request, id):
    """
    Get details of a book by ID.

    GET /api/books/<int:id>/

    Response:
    {
        "bookID": 1,
        "title": "The Great Gatsby",
        "isbn": "9781234567890",
        "published_date": "2022-01-30",
        "genre": "Fiction"
    }
    """
    try:
        book = Book.objects.get(bookID=id)
        serializer = BookSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Book.DoesNotExist:
        return Response({"message": f"Book with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"message": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_book(request, id):
    """
    Update details of a book by ID.

    PUT /api/books/update/<int:id>/

    Request:
    {
        "title": "Updated Title"
    }

    Response:
    {
        "bookID": 1,
        "title": "Updated Title",
        "isbn": "9781234567890",
        "published_date": "2022-01-30",
        "genre": "Fiction"
    }
    """
    try:
        book = Book.objects.get(bookID=id)
    except Book.DoesNotExist:
        return Response({"message": f"Sorry, the book with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookSerializer(book, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Book updated successfully!", "data": serializer.data})
    return Response({"message": "Failed to update the book.", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book(request, id):
    """
    Delete a book by ID.

    DELETE /api/books/delete/<int:id>/

    Response:
    204 No Content - Book successfully deleted
    """
    try:
        book = Book.objects.get(bookID=id)
    except Book.DoesNotExist:
        return Response({"message": f"Sorry, the book with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    book.delete()
    return Response({"message": "Book successfully deleted"}, status=status.HTTP_204_NO_CONTENT)



# BookDetails views
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book_details(request):
    """
    Create details for a book.

    POST /api/book-details/create/

    Request:
    {
        "BookID": 1,
        "number_of_pages": 300,
        "publisher": "Penguin Books",
        "language": "English"
    }

    Response:
    201 Created
    {
        "detailsID": 1,
        "BookID": 1,
        "number_of_pages": 300,
        "publisher": "Penguin Books",
        "language": "English"
    }
    """
    serializer = BookDetailsSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_book_details_by_id(request, id):
    """
    Get details of a book by details ID.

    GET /api/book-details/<int:id>/

    Response:
    200 OK - Book details retrieved successfully
    {
        "detailsID": 1,
        "bookID": 1,
        "number_of_pages": 300,
        "publisher": "Penguin Books",
        "language": "English"
    }
    """
    try:
        book_details = BookDetails.objects.get(detailsID=id)
    except BookDetails.DoesNotExist:
        return Response({"message": f"Sorry, the book details with ID {id} do not exist."}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookDetailsSerializer(book_details)
    return Response({"message": "Book details retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)



@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_book_details(request, id):
    """
    Update details of a book by details ID.

    PUT /api/book-details/update/<int:id>/

    Request:
    {
        "number_of_pages": 350
    }

    Response:
    200 OK - Book details updated successfully
    {
        "detailsID": 1,
        "bookID": 1,
        "number_of_pages": 350,
        "publisher": "Penguin Books",
        "language": "English"
    }
    """
    try:
        book_details = BookDetails.objects.get(detailsID=id)
    except BookDetails.DoesNotExist:
        return Response({"message": f"Sorry, the book details with ID {id} do not exist."}, status=status.HTTP_404_NOT_FOUND)

    serializer = BookDetailsSerializer(book_details, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Book details updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
    return Response({"message": "Failed to update book details", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_book_details(request, id):
    """
    Delete details of a book by details ID.

    DELETE /api/book-details/delete/<int:id>/

    Response:
    204 No Content - Book details successfully deleted
    """
    try:
        book_details = BookDetails.objects.get(detailsID=id)
    except BookDetails.DoesNotExist:
        return Response({"message": f"Sorry, the book details with ID {id} do not exist."}, status=status.HTTP_404_NOT_FOUND)

    book_details.delete()
    return Response({"message": "Book details successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


# BorrowedBooks views

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def borrow_book(request):
    """
    Record the borrowing of a book.

    POST /api/borrow/create/

    Request:
    {
        "userID": 1,
        "bookID": 1,
        "borrow_date": "2022-01-30"
    }

    Response:
    201 Created - Book successfully borrowed
    {
        "userID": 1,
        "bookID": 1,
        "borrow_date": "2022-01-30",
        "return_date": null
    }
    """
    serializer = BorrowedBooksSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Book successfully borrowed", "data": serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"message": "Failed to borrow the book", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_borrowed_book_by_id(request, id):
    """
    Get details of a borrowed book by ID.

    GET /api/borrowed/<int:id>/

    Response:
    200 OK - Borrowed book details retrieved successfully
    {
        "userID": 1,
        "bookID": 1,
        "borrow_date": "2022-01-30",
        "return_date": null
    }
    """
    try:
        borrowed_book = BorrowedBooks.objects.get(id=id)
    except BorrowedBooks.DoesNotExist:
        return Response({"message": f"Sorry, the borrowed book with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    serializer = BorrowedBooksSerializer(borrowed_book)
    return Response({"message": "Borrowed book details retrieved successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def return_borrowed_book(request, id):
    """
    Update the system when a book is returned.

    PUT /api/borrowed/return/<int:id>/

    Request:
    {
        "return_date": "2022-02-15"
    }

    Response:
    200 OK - Book return updated successfully
    {
        "userID": 1,
        "bookID": 1,
        "borrow_date": "2022-01-30",
        "return_date": "2022-02-15"
    }
    """
    try:
        borrowed_book = BorrowedBooks.objects.get(id=id)
    except BorrowedBooks.DoesNotExist:
        return Response({"message": f"Sorry, the borrowed book with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    borrowed_book.return_date = request.data.get('return_date')
    borrowed_book.save()
    serializer = BorrowedBooksSerializer(borrowed_book)
    return Response({"message": "Book return updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_borrowed_book(request, id):
    """
    Delete a borrowed book by ID.

    DELETE /api/borrowed/delete/<int:id>/

    Response:
    204 No Content - Borrowed book successfully deleted
    """
    try:
        borrowed_book = BorrowedBooks.objects.get(id=id)
    except BorrowedBooks.DoesNotExist:
        return Response({"message": f"Sorry, the borrowed book with ID {id} does not exist."}, status=status.HTTP_404_NOT_FOUND)

    borrowed_book.delete()
    return Response({"message": "Borrowed book successfully deleted"}, status=status.HTTP_204_NO_CONTENT)

