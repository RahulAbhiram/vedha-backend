# RECursion Backend

Django REST API backend for the RECursion programming community website.

## Features

- User Authentication (Registration, Login, Logout)
- User Profiles
- Token-based Authentication
- Django Admin Panel

## Local Development

1. **Setup Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Mac/Linux
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Database Setup:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create Superuser:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Development Server:**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile
- `PUT /api/auth/profile/update/` - Update user profile

## Admin Panel

Access Django admin at: `http://127.0.0.1:8000/admin/`

## Deployment

This backend is configured for deployment on Railway/Render/Heroku.

## Environment Variables

- `DEBUG` - Set to False in production
- `SECRET_KEY` - Django secret key
- `DATABASE_URL` - Database connection string (for production)
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
