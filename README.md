# Event Management API

A robust REST API for managing events, built with Django REST Framework. This application allows users to create, view, update, and delete events, as well as register for events created by other users.

![Django REST Framework](https://img.shields.io/badge/Django_REST_Framework-API-red)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## 📋 Features

- **User Authentication**: JWT-based authentication with token refresh
- **User Management**: Registration, login, logout, profile viewing, and password change
- **Event Management**: Create, view, update, and delete events
- **Event Registration**: Register and unregister for events with capacity limits
- **Advanced Filtering**: Search and filter events by various criteria
- **API Documentation**: Interactive API documentation with Swagger/ReDoc
- **Dockerized Deployment**: Easy deployment with Docker and PostgreSQL

## 🛠️ Tech Stack

- **Backend**: Django 5.2, Django REST Framework
- **Authentication**: JWT (SimpleJWT)
- **Database**: PostgreSQL 17
- **Documentation**: drf-yasg (Swagger/ReDoc)
- **Deployment**: Docker, Docker Compose, Gunicorn
- **Additional Tools**: WhiteNoise, Django-filter

## 📝 Prerequisites

- [Docker](https://www.docker.com/get-started) and Docker Compose
- Basic knowledge of REST APIs and Django

## 🚀 Getting Started

### Setting Up with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone https://github.com/zaietsmo/jointoit-task.git
   cd jointoit-task
   ```

2. **Configure environment variables**
   ```bash
   # Copy the example .env file and modify if needed
   cp .env.example .env
   ```

3. **Build and start the Docker containers**
   ```bash
   docker-compose up -d --build
   ```

4. **Create a superuser (optional)**
   ```bash
   docker-compose exec api python manage.py createsuperuser
   ```

5. **Access the API**
   - API: http://localhost:8000/api/v1/
   - API Documentation: http://localhost:8000/swagger/ or http://localhost:8000/redoc/
   - Admin Interface: http://localhost:8000/admin/

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/zaietsmo/jointoit-task.git
   cd event-management-api
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example .env file and modify for local development
   cp .env.example .env
   ```

5. **Set up a PostgreSQL database** or modify settings.py to use SQLite

6. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser**
   ```bash
   python manage.py createsuperuser
   ```

8. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📚 API Documentation

Interactive API documentation is available after starting the server:

- **Swagger UI**: `/swagger/`
- **ReDoc**: `/redoc/`

### API Endpoints

#### Authentication
- `POST /api/v1/users/register/` - Register a new user
- `POST /api/v1/users/token/` - Obtain JWT tokens
- `POST /api/v1/users/token/refresh/` - Refresh JWT token
- `POST /api/v1/users/logout/` - Logout (blacklist token)
- `GET /api/v1/users/me/` - Get authenticated user details
- `POST /api/v1/users/change-password/` - Change user password

#### Events
- `GET /api/v1/events/` - List all events
- `POST /api/v1/events/` - Create a new event
- `GET /api/v1/events/{id}/` - Retrieve a specific event
- `PUT/PATCH /api/v1/events/{id}/` - Update an event (organizer only)
- `DELETE /api/v1/events/{id}/` - Delete an event (organizer only)
- `POST /api/v1/events/{id}/register/` - Register for an event
- `POST /api/v1/events/{id}/unregister/` - Unregister from an event
- `GET /api/v1/events/{id}/registrations/` - List registrations (organizer only)

#### Registrations
- `GET /api/v1/registrations/` - List all events a user is registered for

## ⚙️ Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| SECRET_KEY | Django secret key | None (required) |
| DEBUG | Debug mode | False |
| ALLOWED_HOSTS | Allowed hosts | localhost |
| DB_NAME | Database name | postgres |
| DB_USER | Database user | postgres |
| DB_PASSWORD | Database password | postgres |
| DB_HOST | Database host | db |
| DB_PORT | Database port | 5432 |

## 📂 Project Structure

```
jointoit-task/
├── core/                # Django project settings
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL routing
│   ├── wsgi.py          # WSGI configuration
│   └── asgi.py          # ASGI configuration
├── users/               # User management app
│   ├── views.py         # User-related views
│   ├── serializers.py   # User serializers
│   └── urls.py          # User URL patterns
├── events/              # Events management app
│   ├── models.py        # Event and Registration models
│   ├── views.py         # Event-related views
│   ├── serializers.py   # Event serializers
│   ├── permissions.py   # Custom permissions
│   └── urls.py          # Event URL patterns
├── .env                 # Environment variables
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── requirements.txt     # Python dependencies
├── setup.cfg            # Flake8 settings
└── README.md            # Project documentation
```

## 🧪 Testing

Run the tests with:

```bash
# With Docker
docker-compose exec api python manage.py test

# Local development
python manage.py test
```

### Example Test Cases:

- User registration and authentication
- Event creation, retrieval, update, and deletion
- Event registration and unregistration
- Permission checks (event modifications restricted to organizers)

## 💡 Usage Examples

### Register a New User

```bash
curl -X POST http://localhost:8000/api/v1/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword123",
    "password2": "securepassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

### Obtain Authentication Token

```bash
curl -X POST http://localhost:8000/api/v1/users/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "securepassword123"
  }'
```

### Create an Event

```bash
curl -X POST http://localhost:8000/api/v1/events/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Tech Conference 2023",
    "description": "Annual technology conference",
    "date": "2023-12-15T09:00:00Z",
    "location": "Convention Center",
    "capacity": 200
  }'
```

### Register for an Event

```bash
curl -X POST http://localhost:8000/api/v1/events/1/register/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
