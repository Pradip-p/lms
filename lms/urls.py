from django.urls import path
from django.views.generic import RedirectView
from .views import (
    # User URLs
    create_user, list_users, get_user_by_id, update_user, delete_user,
    # Book URLs
    create_book, list_books, get_book_by_id, update_book, delete_book,
    # BookDetails URLs
    create_book_details, get_book_details_by_id, update_book_details, delete_book_details,
    # BorrowedBooks URLs
    borrow_book, get_borrowed_book_by_id, return_borrowed_book, delete_borrowed_book,
)

urlpatterns = [
    path('', RedirectView.as_view(url='users/list/', permanent=False)),
    
    # User URLs
    path('users/create/', create_user, name='create-user'),
    path('users/list/', list_users, name='list-users'),
    path('users/<int:id>/', get_user_by_id, name='get-user-by-id'),
    path('users/update/<int:id>/', update_user, name='update-user'),
    path('users/delete/<int:id>/', delete_user, name='delete-user'),

    # Book URLs
    path('books/create/', create_book, name='create-book'),
    path('books/list/', list_books, name='list-books'),
    path('books/<int:id>/', get_book_by_id, name='get-book-by-id'),
    path('books/update/<int:id>/', update_book, name='update-book'),
    path('books/delete/<int:id>/', delete_book, name='delete-book'),

    # BookDetails URLs
    path('book-details/create/', create_book_details, name='create-book-details'),
    path('book-details/<int:id>/', get_book_details_by_id, name='get-book-details-by-id'),
    path('book-details/update/<int:id>/', update_book_details, name='update-book-details'),
    path('book-details/delete/<int:id>/', delete_book_details, name='delete-book-details'),

    # BorrowedBooks URLs
    path('borrow/create/', borrow_book, name='borrow-book'),
    path('borrowed/<int:id>/', get_borrowed_book_by_id, name='get-borrowed-book-by-id'),
    path('borrowed/return/<int:id>/', return_borrowed_book, name='return-borrowed-book'),
    path('borrowed/delete/<int:id>/', delete_borrowed_book, name='delete-borrowed-book'),
]
