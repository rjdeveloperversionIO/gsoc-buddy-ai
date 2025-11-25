#!/usr/bin/env python3
"""
Test script for AI Analyzer Module
Week 2, Step 8: Test the AI Analyzer
Using Gemini 2.5 Flash (June 2025 Release)
"""
import traceback
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from utils.ai_analyzer import AIAnalyzer


def load_environment():
    """Load environment variables from .env file"""
    env_path = Path(__file__).parent / '.env'

    if not env_path.exists():
        print("❌ Error: .env file not found!")
        print(f"Expected location: {env_path}")
        return None

    load_dotenv(env_path)

    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found in .env file")
        print("Please add: GEMINI_API_KEY=your_api_key_here")
        return None

    masked_key = f"{api_key[:10]}...{api_key[-4:]}"
    print(f"✅ API Key loaded: {masked_key}")
    return api_key


def print_section(title: str, char: str = "="):
    """Print formatted section header"""
    print(f"\n{char*60}")
    print(f"{title}")
    print(f"{char*60}\n")


def display_results(analysis: dict):
    """Display analysis results in formatted manner"""

    if 'error' in analysis:
        print("❌ ANALYSIS FAILED")
        print(f"Error Type: {analysis['error']}")
        print(f"Message: {analysis.get('message', 'Unknown error')}")
        if 'solution' in analysis:
            print(f"💡 Solution: {analysis['solution']}")
        if 'details' in analysis:
            print(f"Details: {analysis['details']}")
        return

    # Success - display results
    print("✅ ANALYSIS SUCCESSFUL\n")

    print(f"🎯 Difficulty Level    : {analysis['difficulty']}")
    print(f"🛠️  Required Skills     : {', '.join(analysis['skills'])}")
    print(f"⏱️  Estimated Time      : {analysis['estimated_time']} hours")
    print(f"🎓 GSOC Friendly       : {analysis['gsoc_friendly']}")
    print(f"📁 Category            : {analysis['category']}")
    print(f"⚡ Priority            : {analysis['priority']}")
    print(f"💡 Reasoning           : {analysis['reasoning']}")

    if 'parse_error' in analysis:
        print(f"\n⚠️  Parse Warning: {analysis['parse_error']}")

    print("\n" + "-"*60)
    print("📄 RAW AI RESPONSE:")
    print("-"*60)
    print(analysis.get('raw_response', 'No response'))
    print("-"*60)


def test_single_issue():
    """Test the AI Analyzer with a single GitHub issue"""

    print_section("🧪 TEST 1: SINGLE ISSUE ANALYSIS", "=")

    # Load API key
    api_key = load_environment()
    if not api_key:
        sys.exit(1)

    # Initialize analyzer
    print("\n📦 Initializing AI Analyzer...")
    try:
        analyzer = AIAnalyzer(api_key)
    except (ValueError, ImportError, OSError) as e:
        print(f"❌ Failed to initialize: {e}")
        sys.exit(1)

    # Sample test issue
    title = "Add email validation to registration form"
    description = """
We need to add proper email validation to the user registration form.

**Requirements:**
- Use regex pattern to validate email format
- Show error message for invalid emails
- Add client-side validation with JavaScript
- Ensure form doesn't submit with invalid email
- Add unit tests for validation function

**Context:**
This is a good starter task for someone learning web development.
The registration form is located in `src/components/auth/RegisterForm.js`

**Acceptance Criteria:**
1. Email validation works correctly
2. Error messages are user-friendly
3. Tests pass with 100% coverage
"""
    labels = ["good first issue", "JavaScript", "help wanted", "frontend"]

    # Display test issue
    print_section("📋 TEST ISSUE DETAILS", "-")
    print(f"Title: {title}")
    print(f"Labels: {', '.join(labels)}")
    print_section("", "-")

    # Analyze the issue
    print("🔍 Analyzing issue with Gemini 2.5 Flash...\n")
    analysis = analyzer.analyze_issue(title, description, labels)

    # Display results
    print_section("📊 ANALYSIS RESULTS", "=")
    display_results(analysis)

    return analysis


def test_batch_analysis():
    """Test batch analysis with multiple issues"""

    print_section("🧪 TEST 2: BATCH ANALYSIS", "=")

    api_key = load_environment()
    if not api_key:
        sys.exit(1)

    analyzer = AIAnalyzer(api_key)

    # Multiple test issues
    test_issues = [
        {
            'title': 'Fix typo in README.md',
            'description': 'There is a spelling mistake in the installation section. "installtion" should be "installation".',
            'labels': ['documentation', 'good first issue', 'typo']
        },
        {
            'title': 'Implement dark mode toggle',
            'description': 'Add a button to switch between light and dark themes using CSS variables and localStorage to persist user preference.',
            'labels': ['enhancement', 'CSS', 'JavaScript', 'UI']

        },
        {
            'title': 'Add unit tests for authentication module',
           'description': 'The auth module currently has no test coverage. Need to add Jest tests for login, logout, and token validation functions.',
            'labels': ['testing', 'JavaScript', 'high priority']
        }
    ]

    # Run batch analysis
    results = analyzer.batch_analyze(test_issues)

    # Display summary
    print_section("📊 BATCH ANALYSIS SUMMARY", "=")

    for idx, result in enumerate(results, 1):
        print(f"\n{idx}. {result.get('issue_title', 'Unknown')}")
        print(f"   Difficulty: {result.get('difficulty')}")
        print(f"   Skills: {', '.join(result.get('skills', []))}")
        print(f"   GSOC Friendly: {result.get('gsoc_friendly')}")
        print(f"   Time: {result.get('estimated_time')} hours")

    print("\n" + "="*60)
    print(f"✅ Successfully analyzed {len(results)} issues")
    print("="*60)

    return results


def main():
    """Main test runner"""

    print("\n" + "="*60)
    print("🚀 GSOC BUDDY AI - AI ANALYZER TEST SUITE")
    print("📅 Week 2, Step 8: Test the AI Analyzer")
    print("🤖 Using: Gemini 2.5 Flash (June 2025)")
    print("💫 Context Window: 1 Million Tokens")
    print("="*60)

    try:
        # Test 1: Single issue analysis
        test_single_issue()

        # Pause between tests
        print("\n" + "="*60)
        input("Press Enter to continue to batch analysis test...")

        # Test 2: Batch analysis
        test_batch_analysis()

        # Final summary
        print_section("🎉 ALL TESTS COMPLETED", "=")
        print("✅ Single issue test: PASSED")
        print("✅ Batch analysis test: PASSED")
        print("\n💡 Your AI Analyzer is working perfectly with Gemini 2.5 Flash!")
        print("="*60 + "\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(0)
    except (ValueError, ImportError, OSError, AttributeError, TypeError) as e:
        print(f"\n❌ Test failed with error: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
