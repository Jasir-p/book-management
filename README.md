# Django Book Management API

A Django REST API for managing books, users, and reading lists with full CRUD operations and user authentication.

## Features

- **User Management**: Registration, login, profile management
- **Book Management**: Create, read, update, delete books with metadata
- **Reading Lists**: Personal reading lists with custom ordering
- **Authentication**: Token-based authentication and authorization
- **Error Handling**: Comprehensive error responses with validation

## Requirements

- Python 3.8+
- Django 4.2+
- Django REST Framework 3.14+
- PostgreSQL (recommended) or SQLite for development

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Jasir-p/book-management.git
cd bookmangement
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS="*"
CORS_ALLOWED_ORIGINS="http://localhost:8000"
DB_ENGINE="your-db-engine-postgres-recommended"
DB_NAME="your-db-name"
DB_USER="your-db-user"
DB_PASSWORD="your-db-password"
DB_HOST="your-db-host-or-default-localhost"
DB_PORT="your-db-port-or-default-5432"
```

### 5. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Optional: for admin access
```

### 6. Run the Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Documentation

### Base URL
```
http://localhost:8000/api/
```

### Authentication

The API uses Token-based authentication. Include the token in the Authorization header:

```
Authorization: Token <your-token-here>
```


### Request/Response Examples

#### User Registration
```bash
POST /api/users/
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password123",
}
Response(201 Created):
{
    "id": 5,
   "username": "john_doe",
   "email": "john@example.com"
}
```

#### User Login
```bash
POST /api/users/login/
Content-Type: application/json

{
  "username": "john_doe",
  "password": "secure_password123",
}

Response(200 ok):
{
    "refresh": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "access": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

#### User Profile
```bash
GET /api/users/id=2/
{
    "id": 5,
   "username": "john_doe",
   "email": "john@example.com"
}
```

#### List All Book
```bash
GET /api/book-management/
Retrive all books

[
    {
        "id": 17,
        "title": "The wave",
        "genre": "Programming",
        "description": "A deep dive into advanced Python concepts.",
        "author": [
            "jasi",
            "jiju"
        ],
        "publication_date": "2025-08-11"
    },
    {
        "id": 18,
        "title": "The waves",
        "genre": "Programmingss",
        "description": "A deep dive into advanced Python concepts.",
        "author": [
            "jasi",
            "jiju"
        ],
        "publication_date": "2025-08-11"
    },
    {
        "id": 11,
        "title": "The Sic artist",
        "genre": "Psycology",
        "description": "A deep dive into advanced Sycology concepts.",
        "author": [
            "jasi"
        ],
        "publication_date": "2025-08-09"
    },
    {
        "id": 15,
        "title": "The Si artist",
        "genre": "Psycology",
        "description": "A deep dive into advanced Sycology concepts.",
        "author": [
            "jasi"
        ],
        "publication_date": "2025-08-09"
    }
]
```

#### Create Book
```bash
POST /api/book-management/
Authorization: Token <your-token>
Content-Type: application/json

{
  "title": "The Great Gatsby",
  "authors": ["F. Scott Fitzgerald"],
  "genre": "Fiction",
  "description": "A classic American novel set in the Jazz Age."
}

Response
```

#### Create Reading List
```bash
POST /api/reading-lists/
Authorization: Token <your-token>
Content-Type: application/json

{
  "name": "Summer Reading 2024",
  "description": "Books to read during summer vacation"
}
```

#### Add Book to Reading List
```bash
POST /api/reading-lists/1/add-book/
Authorization: Token <your-token>
Content-Type: application/json

{
  "book_id": 5,
  "order": 1
}
```

## Data Models

### User
- `username` (unique)
- `email` (unique)
- `first_name`
- `last_name`
- `date_joined`

### Book
- `title`
- `authors` (JSONField - list of strings)
- `genre`
- `publication_date`
- `description` (optional)
- `created_by` (ForeignKey to User)
- `created_at`
- `updated_at`

### ReadingList
- `name`
- `description` (optional)
- `owner` (ForeignKey to User)
- `created_at`
- `updated_at`

### ReadingListItem
- `reading_list` (ForeignKey to ReadingList)
- `book` (ForeignKey to Book)
- `order` (IntegerField for custom ordering)
- `added_at`

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `409 Conflict`: Resource already exists
- `500 Internal Server Error`: Server error

Example error response:
```json
{
  "error": "Validation failed",
  "details": {
    "email": ["This field is required."],
    "username": ["This field must be unique."]
  }
}
```

## Testing

Run the test suite:

```bash
python manage.py test
```

Run with coverage:

```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates HTML coverage report
```

## Development

### Project Structure
```
book-management-api/
├── manage.py
├── requirements.txt
├── .env.example
├── book_management/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── users/
│   ├── books/
│   └── reading_lists/
```

### Adding New Features

1. Create new app: `python manage.py startapp app_name`
2. Add to `INSTALLED_APPS` in settings.py
3. Create models, serializers, views, and URLs
4. Write tests
5. Update API documentation

## Deployment

For production deployment:

1. Set `DEBUG=False` in environment
2. Configure proper database (PostgreSQL recommended)
3. Set up static files serving
4. Use production WSGI server (gunicorn)
5. Configure reverse proxy (nginx)
6. Set up SSL certificate

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request



## Support

For questions or issues, please create an issue in the repository or contact [your-email@example.com].
