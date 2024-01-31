# Django Library System API

This Django project serves as the backend API for a library system. It includes endpoints to manage CustomUsers, books, book details, and borrowed books.

## Table of Contents

- [Project Setup](#project-setup)
  - [Python Environment Setup](#python-environment-setup)
  - [Install Requirements](#install-requirements)
  - [Database Configuration](#database-configuration)
- [Database Schema Design](#database-schema-design)
- [API Development](#api-development)
  - [CustomUser APIs](#CustomUser-apis)
  - [Book APIs](#book-apis)
  - [BookDetails APIs](#bookdetails-apis)
  - [BorrowedBooks APIs](#borrowedbooks-apis)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Setup

### Python Environment Setup

1. Install [Python](https://www.python.org/) (version 3.6 or higher).

2. Create a virtual environment:

   ```bash
   python -m venv venv

### Install Requirements
1. Install project dependencies:
```
pip install -r requirements.txt

```

### Database Configuration

2. Run migrations:
```
python manage.py migrate
```
3. Running Tests
Run tests to ensure everything is set up correctly:
```python manage.py test lms
```

### Database Schema Design
The following models with specified attributes and relationships:

## CustomUser Model

- Attributes: userID, Name, Email, MembershipDate
- Relationships: 1-M with BorrowedBooks (A CustomUser can borrow multiple books)

## Book Model

- Attributes: BookID, Title, ISBN, PublishedDate, Genre
- Relationships: 1-1 with BookDetails (Each book has one set of details)

## BookDetails Model (for 1-1 relationship)

- Attributes: DetailsID, BookID (FK), NumberOfPages, Publisher, Language
- Relationships: 1-1 with Book (Each set of book details is linked to exactly one book)

## BorrowedBooks Model (to demonstrate 1-N relationship)

- Attributes: userID (FK), BookID (FK), BorrowDate, ReturnDate
- Relationships: 1-M with CustomUser (A CustomUser can borrow multiple books)

## API Development

Develop the following APIs for each model:

### CustomUser APIs

1. **Create a New CustomUser:**
   - Endpoint to add a new CustomUser to the system with details like name, email, and membership date.

2. **List All CustomUsers:**
   - Endpoint to retrieve a list of all CustomUsers in the system.

3. **Get CustomUser by ID:**
   - Endpoint to fetch a CustomUser's details using their userID.

### Book APIs

1. **Add a New Book:**
   - Endpoint to add a new book record, including title, ISBN, published date, and genre.

2. **List All Books:**
   - Endpoint to retrieve a list of all books in the library.

3. **Get Book by ID:**
   - Endpoint to fetch details of a specific book using its BookID.

4. **Assign/Update Book Details:**
   - Endpoint to assign details to a book or update existing book details, like the number of pages, publisher, language.

### BorrowedBooks APIs

1. **Borrow a Book:**
   - Endpoint to record the borrowing of a book by linking a CustomUser with a book.

2. **Return a Book:**
   - Endpoint to update the system when a book is returned.

3. **List All Borrowed Books:**
   - Endpoint to list all books currently borrowed from the library.

## Usage

Start the Django development server:

```bash
python manage.py runserver


Access the API at http://localhost:8000/.




