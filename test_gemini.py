"""
Test script to verify Google Gemini API is working.
Run this to confirm your API key is valid.
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai


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
    genai.configure(api_key=api_key)

    # Create model instance
    model = genai.GenerativeModel('gemini-pro')

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

    except Exception as error:
        print(f"\n❌ ERROR: {str(error)}")
        print("\nPossible issues:")
        print("1. Invalid API key")
        print("2. API quota exceeded")
        print("3. Network connection problem")


if __name__ == "__main__":
    test_gemini_api()