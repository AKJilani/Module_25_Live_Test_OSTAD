# Social Media Application

A Django-based social media platform that allows users to create, read, update, and delete posts. The application features user authentication, a global feed, and personalized profile pages.

## Features

- **User Authentication**
  - Registration with username, email, and password
  - Login/logout functionality
  - Secure password management

- **Post Management**
  - Global feed showing posts from all users
  - Personal profile page with user-specific posts
  - Create new posts with text and optional images
  - Edit and delete functionality for own posts

- ## Search Functionality
  - Have Search Function for Home Page
      --Sort by Date
      --Media Type
      --Filter by User
      --Search Box
  - Have Search Function for Profile Page
      --Sort by Date
      --Media Type
      -- Search Box

- **User Interface**
  - Clean and intuitive navigation
  - Responsive design
  - Consistent layout using template inheritance
  - User feedback messages for actions

## Technology Stack

- Backend: Django 5.1.6
- Frontend: HTML, CSS, JavaScript
- Database: SQLite
- Image Handling: Pillow 11.1.0

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/AKJilani/Module_25_Live_Test_OSTAD.git
   cd SocialAPP
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Visit `http://127.0.0.1:8000` in your web browser

## Test Credentials

### Superuser Account
- Username: admin
- Password: admin

### Sample User Accounts
1. First Test User
   - Username: A.K.Jilani
   - Password: Admin@6261

2. Second Test User
   - Username: habib
   - Password: admin@123

#### Added 2 different ERD (with and without) Relation between Database Tables.
   ---ERD TITLES:
   - File Name: ERD_With_Relationship.jpg
   - SocialAPP_ERD.jpg

## Project Structure

```
Social_Media_App/
├── media/
├── social_app/
│   ├── __pycache__/
│   └── migrations/
├── templatetags/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── custom_filters.py
│   ├── form_tags.py
│   └── models.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── social_project/
│   ├── __pycache__/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/
│   └── js/
│       └── comments.js
├── templates/
│   ├── registration/
│   │   └── login.html
│   ├── social_app/
│   │   ├── home.html
│   │   ├── landing.html
│   │   ├── post_confirm_delete.html
│   │   ├── post_form.html
│   │   ├── profile.html
│   │   └── register.html
│   └── base.html
├── venv/
├── create_users.py
├── db.sqlite3
├── manage.py
└── requirements.txt

```

## Dependencies

```
asgiref==3.8.1
Django==5.1.6
pillow==11.1.0
sqlparse==0.5.3
tzdata==2025.1
```

## Key Features Implementation

1. **Global Feed**
   - Displays posts from all users
   - Optimized database queries using Django's ORM
   - Paginated results for better performance

2. **Profile Page**
   - User-specific post management
   - Edit and delete functionality
   - Secure access control

3. **Post Management**
   - Create posts with text and optional images
   - Update and delete own posts
   - Confirmation before deletion

4. **Authentication**
   - Django's built-in authentication system
   - Protected routes using login_required decorator
   - User session management

## Security Features

- CSRF protection enabled
- Secure password hashing
- User-specific content protection
- Login required for sensitive operations

## Best Practices

- Template inheritance for consistent UI
- Query optimization for better performance
- Clean code structure following Django conventions
- Proper error handling and user feedback

## Contributing

This is an assignment project and is not open for contributions.

## License

This project is created for educational purposes as part of a Django development assignment.