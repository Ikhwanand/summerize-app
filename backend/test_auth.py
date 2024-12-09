import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base URL for the backend
BASE_URL = "http://localhost:8000"

def test_registration():
    print("Testing Registration...")
    registration_url = f"{BASE_URL}/auth/registration/"
    
    # Test data
    registration_data = {
        "email": "testuser@example.com",
        "password1": "TestPassword123!",
        "password2": "TestPassword123!"
    }
    
    try:
        response = requests.post(registration_url, json=registration_data)
        print("Registration Response Status:", response.status_code)
        print("Registration Response JSON:", response.json())
    except Exception as e:
        print(f"Registration Error: {e}")

def test_login():
    print("Testing Login...")
    login_url = f"{BASE_URL}/auth/login/"
    
    # Test data
    login_data = {
        "email": "testuser@example.com",
        "password": "TestPassword123!"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        print("Login Response Status:", response.status_code)
        print("Login Response JSON:", response.json())
    except Exception as e:
        print(f"Login Error: {e}")

def main():
    print("Starting Authentication Endpoint Tests...")
    test_registration()
    test_login()

if __name__ == "__main__":
    main()
