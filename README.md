# Library Management System API

A RESTful Library Management System developed using FastAPI, Pydantic, SQLAlchemy ORM, and MySQL.

The application manages categories, books, members, book borrowing, returns, overdue books, and borrowing history.

## Technologies Used

- Python
- FastAPI
- Pydantic
- SQLAlchemy ORM
- MySQL
- PyMySQL
- Uvicorn
- python-dotenv

## Project Structure

```text
library_management/
│
├── app/
│   ├── main.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── borrow.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── category.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── borrow.py
│   │
│   ├── services/
│   │   ├── category.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── borrow.py
│   │
│   └── routers/
│       ├── category.py
│       ├── book.py
│       ├── member.py
│       └── borrow.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Features

### Category Management

- Add new categories
- View all categories
- Update categories
- Delete categories
- Unique category name validation
- Pagination support

### Book Management

- Add new books
- View all books
- View a book by ID
- Update books
- Delete books
- Unique ISBN validation
- Search books by title
- Search books by author
- Filter books by category
- Pagination support
- Track total and available copies

### Member Management

- Add new members
- View all members
- View a member by ID
- Update members
- Delete members
- Unique email validation
- Email format validation
- Phone number validation
- Active and inactive member status
- Pagination support

### Borrow and Return Management

- Borrow books
- Return books
- View books currently borrowed by a member
- View book borrowing history
- View overdue books
- Automatically calculate due dates
- Automatically update available book copies

## Business Rules

- A book cannot be borrowed when no copies are available.
- Available copies decrease when a book is borrowed.
- Available copies increase when a book is returned.
- A member can borrow a maximum of 3 books at a time.
- A member cannot borrow the same book twice without returning it.
- Inactive members cannot borrow books.
- The due date is automatically calculated as 14 days from the borrow date.
- Books that pass their due date without being returned are marked as overdue.
- A currently borrowed book cannot be deleted.
- A member with active borrowed books cannot be deleted.

## API Endpoints

### Category APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/categories` | Create a category |
| GET | `/categories` | View categories |
| PUT | `/categories/{category_id}` | Update a category |
| DELETE | `/categories/{category_id}` | Delete a category |

### Book APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/books` | Add a book |
| GET | `/books` | View books |
| GET | `/books/{book_id}` | View a book by ID |
| PUT | `/books/{book_id}` | Update a book |
| DELETE | `/books/{book_id}` | Delete a book |

Book filtering example:

```text
/books?author=narayan&category_id=1&skip=0&limit=10
```

### Member APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/members` | Add a member |
| GET | `/members` | View members |
| GET | `/members/{member_id}` | View a member by ID |
| PUT | `/members/{member_id}` | Update a member |
| DELETE | `/members/{member_id}` | Delete a member |

### Borrow and Return APIs

| Method | Endpoint | Description |
|---|---|---|
| POST | `/borrow` | Borrow a book |
| PUT | `/return/{borrow_id}` | Return a book |
| GET | `/members/{member_id}/books` | View books borrowed by a member |
| GET | `/books/{book_id}/borrow-history` | View a book's borrow history |
| GET | `/borrow/overdue` | View overdue borrow records |

## Setup

### 1. Create Virtual Environment

```powershell
python -m venv .venv
```

### 2. Activate Virtual Environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If you are using Command Prompt:

```cmd
.venv\Scripts\activate
```

### 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

## Database Setup

Create the MySQL database:

```sql
CREATE DATABASE library_db;
```

Create a `.env` file in the project root.

Example:

```text
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/library_db
```

If the MySQL password contains special characters such as `@`, URL-encode them in the database URL.

For example, `@` becomes `%40`.

Do not upload the `.env` file to GitHub because it contains database credentials.

## Run the Application

Start the FastAPI development server:

```powershell
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

## HTTP Status Codes

The API uses appropriate HTTP status codes:

- `200 OK` - Request completed successfully
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid business data
- `404 Not Found` - Requested resource was not found
- `409 Conflict` - Duplicate data or business rule conflict
- `422 Unprocessable Entity` - Request validation failed

## Security

Database credentials are stored in the `.env` file.

The `.env` file is excluded from Git using `.gitignore`.

```text
.env
```

Never commit database passwords or other sensitive credentials to GitHub.

## Author

Dammuru Somalinga