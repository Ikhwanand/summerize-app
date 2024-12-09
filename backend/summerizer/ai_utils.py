import os 
import re
import requests
from pytube import YouTube
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_video_info(url: str) -> dict:
    """Get video information from YouTube URL"""
    try:
        # Normalize the YouTube URL
        normalized_url = normalize_youtube_url(url)
        
        # Try pytube first
        try:
            yt = YouTube(normalized_url)
            
            # Validate video information
            if not yt.title:
                raise ValueError("Video title is empty")
            
            # Handle cases with no description
            description = yt.description or "No description available"
            
            return {
                'title': yt.title,
                'thumbnail_url': yt.thumbnail_url,
                'duration': str(yt.length),
                'description': description,
            }
        except Exception as pytube_error:
            # If pytube fails, try an alternative method
            return fetch_video_info_alternative(normalized_url)
    
    except Exception as e:
        raise ValueError(f"Error fetching video info: {str(e)}")

def normalize_youtube_url(url: str) -> str:
    """Normalize YouTube URL to ensure compatibility"""
    # Remove any additional parameters
    base_url = url.split('&')[0]
    
    # Ensure standard YouTube URL format
    if 'youtu.be' in base_url:
        video_id = base_url.split('/')[-1]
        return f"https://www.youtube.com/watch?v={video_id}"
    
    return base_url

def fetch_video_info_alternative(url: str) -> dict:
    """Alternative method to fetch video information"""
    try:
        # Use YouTube's embed page to extract metadata
        embed_url = f"https://www.youtube.com/oembed?url={url}&format=json"
        response = requests.get(embed_url)
        
        if response.status_code == 200:
            embed_data = response.json()
            
            # Fetch description using another method
            description = fetch_video_description(url)
            
            return {
                'title': embed_data.get('title', 'Unknown Title'),
                'thumbnail_url': embed_data.get('thumbnail_url', ''),
                'duration': 'Unknown',  # Cannot get duration from this method
                'description': description
            }
        else:
            raise ValueError(f"Failed to fetch video info. Status code: {response.status_code}")
    
    except Exception as e:
        raise ValueError(f"Alternative video info fetch failed: {str(e)}")

def fetch_video_description(url: str) -> str:
    """Attempt to fetch video description using web scraping"""
    try:
        # Use requests to fetch the YouTube page
        response = requests.get(url)
        
        if response.status_code == 200:
            # Use regex to extract description
            description_match = re.search(r'"shortDescription":"(.*?)"', response.text)
            
            if description_match:
                # Unescape the description
                description = description_match.group(1).encode('utf-8').decode('unicode-escape')
                return description
        
        return "No description available"
    
    except Exception as e:
        return "Unable to fetch description"

def generate_summary(text:str) -> str:
    """Generate summary using OpenAI or fallback method"""
    try:
        # Validate input text
        if not text or len(text.strip()) < 10:
            return "Unable to generate summary due to insufficient content."
        
        # Truncate very long descriptions to avoid token limits
        if len(text) > 5000:
            text = text[:5000]
        
        try:
            response = openai.ChatCompletion.create(
                model='gpt-3.5-turbo',
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes video content concisely with important details."},
                    {"role": "user", "content": f"Please provide a concise summary of this video content: {text}"}
                ],
                max_tokens=425  # Optimal token range
            )
            
            # Extract the summary from the response
            summary = response.choices[0].message['content'].strip()
            
            # Validate summary
            if not summary:
                return generate_fallback_summary(text)
            
            return summary
        
        except Exception as openai_error:
            # Log the specific OpenAI error
            print(f"OpenAI Error: {openai_error}")
            
            # Fallback to alternative summary generation
            return generate_fallback_summary(text)
    
    except Exception as e:
        # Handle any unexpected errors
        print(f"Unexpected error in summary generation: {e}")
        return generate_fallback_summary(text)

def generate_fallback_summary(text: str) -> str:
    """Generate a simple extractive summary when OpenAI fails"""
    try:
        # Split text into sentences
        sentences = text.split('.')
        
        # Select first 2-3 sentences as summary
        summary_sentences = sentences[:3]
        
        # Join sentences and add ellipsis if truncated
        summary = '. '.join(summary_sentences).strip() + ('...' if len(sentences) > 3 else '')
        
        return summary if summary else "No summary could be generated."
    
    except Exception as e:
        print(f"Fallback summary generation error: {e}")
        return "Unable to generate summary."