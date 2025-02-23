import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_project.settings')
django.setup()

from django.contrib.auth.models import User

users_data = [
    {'username': 'user1', 'email': 'user1@example.com', 'password': 'user1password'},
    {'username': 'user2', 'email': 'user2@example.com', 'password': 'user2password'},
]

for user_data in users_data:
    if not User.objects.filter(username=user_data['username']).exists():
        User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        print(f"Created user: {user_data['username']}")
    else:
        print(f"User {user_data['username']} already exists")