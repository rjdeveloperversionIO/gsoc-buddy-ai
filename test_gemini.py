"""
Test script to verify Google Gemini API is working.
Run this to confirm your API key is valid.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions


def test_gemini_api() -> None:
    """Test the Gemini API connection and basic functionality."""
    # Load environment variables from .env file
    load_dotenv()

    # Get API key from environment
    api_key = os.getenv("GEMINI_API_KEY")

    # Check if API key exists
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file")
        print("Please add your API key to .env file:")
        print("GEMINI_API_KEY=your-api-key-here")
        return

    print(f"✅ API key loaded: {api_key[:10]}...{api_key[-4:]}")

    # Configure Gemini
    try:
        genai.configure(api_key=api_key)
    except ValueError as error:
        print(f"❌ ERROR: Invalid API key format: {error}")
        return

    # Create model instance with UPDATED model name
    try:
        # Use gemini-1.5-flash (free, fast, recommended)
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Model initialized: gemini-1.5-flash")
    except (ValueError, TypeError) as error:
        print(f"❌ ERROR: Failed to create model: {error}")
        return

    print("\n🤖 Testing Gemini AI...")

    # Test prompt
    test_prompt = """
    Analyze this GitHub issue and extract information:

    Title: Add input validation to login form
    Description: The login form currently accepts any input.
    We need to add email validation using regex and check password strength.
    Good for beginners who know JavaScript and HTML.

    Extract:
    1. Difficulty level (beginner/intermediate/advanced)
    2. Required skills (programming languages and technologies)
    3. Estimated time to complete
    4. Is this good for GSOC beginners?
    """

    try:
        # Generate response
        response = model.generate_content(test_prompt)

        print("\n✅ SUCCESS! Gemini AI responded:\n")
        print("=" * 60)
        print(response.text)
        print("=" * 60)
        print("\n🎉 Your Gemini API is working perfectly!")

    except google_exceptions.InvalidArgument as error:
        print("\n❌ ERROR: Invalid API key")
        print(f"Details: {error}")
        print("\nSolution:")
        print("1. Go to https://aistudio.google.com/app/apikey")
        print("2. Create a new API key")
        print("3. Update your .env file with the new key")

    except google_exceptions.PermissionDenied as error:
        print("\n❌ ERROR: Permission denied")
        print(f"Details: {error}")
        print("\nSolution:")
        print("1. Check if your API key is valid")
        print("2. Ensure the Generative AI API is enabled")

    except google_exceptions.ResourceExhausted as error:
        print("\n❌ ERROR: API quota exceeded")
        print(f"Details: {error}")
        print("\nSolution:")
        print("1. Wait a few minutes before trying again")
        print("2. Free tier: 15 requests per minute for gemini-2.5-flash")

    except google_exceptions.NotFound as error:
        print("\n❌ ERROR: Model not found")
        print(f"Details: {error}")
        print("\nSolution:")
        print("1. The model name may have changed")
        print("2. Run 'python check_models.py' to see available models")

    except google_exceptions.GoogleAPIError as error:
        print("\n❌ ERROR: Google API error occurred")
        print(f"Details: {error}")
        print("\nSolution:")
        print("1. Check your internet connection")
        print("2. Verify API key is correct")
        print("3. Try again in a few moments")

    except ConnectionError as error:
        print("\n❌ ERROR: Network connection problem")
        print(f"Details: {error}")
        print("\nSolution:")
        print("1. Check your internet connection")
        print("2. Try accessing https://google.com in browser")

    except TimeoutError as error:
        print("\n❌ ERROR: Request timed out")
        print(f"Details: {error}")
        print("\nSolution:")
        print("1. Check your internet connection speed")
        print("2. Try again - the API might be slow")

if __name__ == "__main__":
    test_gemini_api()
