import os
import django
from django.core.wsgi import get_wsgi_application

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
get_wsgi_application()

# Import after Django setup
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

def create_test_user():
    email = "testuser@example.com"
    password = "TestPassword123!"
    
    # Get the User model
    User = get_user_model()
    
    # Check if user already exists
    if User.objects.filter(email=email).exists():
        print(f"User {email} already exists.")
        return
    
    # Create new user
    try:
        # Create user with email as username
        user = User.objects.create_user(
            email=email, 
            username=email,  # Use email as username
            password=password
        )
        
        # Verify email address
        EmailAddress.objects.create(
            user=user,
            email=email,
            verified=True,
            primary=True
        )
        
        print(f"Test user {email} created successfully!")
    except Exception as e:
        print(f"Error creating user: {e}")

if __name__ == "__main__":
    create_test_user()
