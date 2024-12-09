import requests
import os
import traceback
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_auth_token():
    """Get authentication token by logging in"""
    login_url = "http://localhost:8000/auth/login/"
    login_data = {
        "email": "testuser@example.com",
        "password": "TestPassword123!"
    }
    
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            return response.json()['key']
        else:
            print("Login failed:", response.json())
            print("Response Status Code:", response.status_code)
            print("Response Text:", response.text)
            return None
    except Exception as e:
        print(f"Login Error: {e}")
        print(traceback.format_exc())
        return None

def test_summarize(token, youtube_url):
    """Test summarization endpoint"""
    summarize_url = "http://localhost:8000/api/summaries/summarize/"
    
    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "url": youtube_url
    }
    
    try:
        # Print environment variables for debugging
        print("OPENAI_API_KEY:", "PRESENT" if os.getenv("OPENAI_API_KEY") else "MISSING")
        
        # Validate URL
        if not youtube_url.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
            raise ValueError(f"Invalid YouTube URL: {youtube_url}")
        
        response = requests.post(summarize_url, json=data, headers=headers)
        
        # Print full response details for debugging
        print("Response Status Code:", response.status_code)
        print("Response Headers:", response.headers)
        print("Response Text:", response.text)
        
        # Try to parse JSON response
        try:
            response_data = response.json()
            print("Response JSON:", response_data)
        except ValueError:
            print("Failed to parse JSON response")
            print("Response Text:", response.text)
            raise
        
        # Assert response status code
        assert response.status_code == 200, f"Expected 200 status code, got {response.status_code}. Response: {response.text}"
        
        # Validate response structure
        assert 'title' in response_data, "Response missing 'title'"
        assert 'summary' in response_data, "Response missing 'summary'"
        assert 'thumbnail_url' in response_data, "Response missing 'thumbnail_url'"
        
        # Print out some basic info for verification
        print("Video Title:", response_data['title'])
        print("Summary Length:", len(response_data['summary']))
        print("Thumbnail URL:", response_data['thumbnail_url'])
        
        return response_data
    except AssertionError as ae:
        print(f"Assertion Error: {ae}")
        print(traceback.format_exc())
        raise
    except Exception as e:
        print(f"Summarization Error: {e}")
        print(traceback.format_exc())
        raise

def main():
    # Test YouTube URLs (multiple for robustness)
    test_urls = [
        "https://www.youtube.com/watch?v=MPN0ae2KM3w",  # Original URL
        "https://youtu.be/MPN0ae2KM3w",  # Shortened URL
        "https://www.youtube.com/watch?v=MPN0ae2KM3w&feature=youtu.be"  # URL with additional parameters
    ]
    
    # Get authentication token
    token = get_auth_token()
    
    if token:
        print("Authentication Token:", token)
        
        # Try multiple URLs
        for url in test_urls:
            try:
                print(f"\nTesting URL: {url}")
                test_summarize(token, url)
                break  # Stop if one URL works
            except Exception as e:
                print(f"Failed with URL {url}: {e}")
                continue
    else:
        print("Failed to obtain authentication token")

if __name__ == "__main__":
    main()
