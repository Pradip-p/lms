from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser, Book, BookDetails, BorrowedBooks
from rest_framework.authtoken.models import Token

class LMSTestCase(APITestCase):
    def setUp(self):
        self.register_url = reverse('create-user')
        self.list_users_url = reverse('list-users')
        self.get_user_by_id_url = reverse('get-user-by-id', args=[1])  # Assuming user ID 1 exists
        self.update_user_url = reverse('update-user', args=[1])  # Assuming user ID 1 exists
        self.delete_user_url = reverse('delete-user', args=[1])  # Assuming user ID 1 exists
        self.create_book_url = reverse('create-book')
        self.list_books_url = reverse('list-books')
        self.get_book_by_id_url = reverse('get-book-by-id', args=[1])  # Assuming book ID 1 exists
        self.update_book_url = reverse('update-book', args=[1])  # Assuming book ID 1 exists
        self.delete_book_url = reverse('delete-book', args=[1])  # Assuming book ID 1 exists
        self.create_book_details_url = reverse('create-book-details')
        self.get_book_details_by_id_url = reverse('get-book-details-by-id', args=[1])  # Assuming details ID 1 exists
        self.update_book_details_url = reverse('update-book-details', args=[1])  # Assuming details ID 1 exists
        self.delete_book_details_url = reverse('delete-book-details', args=[1])  # Assuming details ID 1 exists
        self.borrow_book_url = reverse('borrow-book')
        self.get_borrowed_book_by_id_url = reverse('get-borrowed-book-by-id', args=[1])  # Assuming borrowed book ID 1 exists
        self.return_borrowed_book_url = reverse('return-borrowed-book', args=[1])  # Assuming borrowed book ID 1 exists
        self.delete_borrowed_book_url = reverse('delete-borrowed-book', args=[1])  # Assuming borrowed book ID 1 exists

        self.user_data = {
            "name": "John Thapa",
            "email": "john@example.com",
            "password": "secure_password"
        }

        self.book_data = {
            "title": "The Great Gatsby",
            "isbn": "978123890",
            "published_date": "2022-01-30",
            "genre": "Fiction"
        }
        
        self.book_details_data = {
            "bookID": 1,
            "number_of_pages": 300,
            "publisher": "Penguin Books",
            "language": "English"
        }

        self.borrowed_book_data = {
            "userID": 1,
            "bookID": 1,
            "borrow_date": "2022-01-30"
        }

        # Create some users for testing
        self.user1 = CustomUser.objects.create(name="John Thapa", email="john12@example.com", password="secure_password")
        self.user2 = CustomUser.objects.create(name="Alice Doe", email="alice@example.com", password="another_password")
        
        # Create some books for testing
        self.book1 = Book.objects.create(title="The Great Adventure", published_date="2022-01-30",genre="comedy", isbn="123457890")
        self.book2 = Book.objects.create(title="Mystery of the Lost Key",published_date="2022-01-30", genre="romantic", isbn="09854321")
                
        # Create a user and get or create a token for authentication
        self.user = CustomUser.objects.create(name="John Doe", email="john.doe@example.com", password="test_password")
        self.token, created = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')


    def test_create_user(self):
        # Send a POST request to create a new user
        response = self.client.post(self.register_url, self.user_data, format='json')

        # Check if the response status code is 201 (HTTP Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_users(self):
        # Test listing all users
        response = self.client.get(self.list_users_url)
        # Check if the response status code is 200 (HTTP OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_nonexistent_user_by_id(self):
        # Test getting a user by ID that doesn't exist
        response = self.client.get(reverse('get-user-by-id', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_user(self):
        # Test updating a user that doesn't exist
        response = self.client.put(reverse('update-user', args=[999]), self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_user(self):
        # Test deleting a user that doesn't exist
        response = self.client.delete(reverse('delete-user', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_create_book(self):
        response = self.client.post(self.create_book_url, self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_books(self):
        # Test listing all books
        response = self.client.get(self.list_books_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_nonexistent_book_by_id(self):
        # Test getting a book by ID that doesn't exist
        response = self.client.get(reverse('get-book-by-id', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_book(self):
        # Test updating a book that doesn't exist
        response = self.client.put(reverse('update-book', args=[999]), self.book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_book(self):
        # Test deleting a book that doesn't exist
        response = self.client.delete(reverse('delete-book', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_book_details(self):
        response = self.client.post(self.create_book_details_url, self.book_details_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_nonexistent_book_details_by_id(self):
        # Test getting book details by ID that doesn't exist
        response = self.client.get(reverse('get-book-details-by-id', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_nonexistent_book_details(self):
        # Test updating book details that doesn't exist
        response = self.client.put(reverse('update-book-details', args=[999]), self.book_details_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_book_details(self):
        # Test deleting book details that doesn't exist
        response = self.client.delete(reverse('delete-book-details', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_borrow_book(self):
        response = self.client.post(self.borrow_book_url, self.borrowed_book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_nonexistent_borrowed_book_by_id(self):
        # Test getting borrowed book by ID that doesn't exist
        response = self.client.get(reverse('get-borrowed-book-by-id', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_return_nonexistent_borrowed_book(self):
        # Test returning borrowed book by ID that doesn't exist
        response = self.client.put(reverse('return-borrowed-book', args=[999]), {"return_date": "2022-02-15"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_borrowed_book(self):
        # Test deleting borrowed book by ID that doesn't exist
        response = self.client.delete(reverse('delete-borrowed-book', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



