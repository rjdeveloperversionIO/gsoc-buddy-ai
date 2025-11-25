#!/usr/bin/env python3
"""
AI Analyzer Module for GitHub Issue Classification
Uses Google Gemini 2.5 Flash AI to analyze and classify GitHub issues
"""

import os
from typing import Dict, Optional, List
import google.generativeai as genai
from google.api_core import exceptions as google_exceptions


class AIAnalyzer:
    """Handles AI-powered analysis of GitHub issues using Gemini 2.5 Flash"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize AI Analyzer with Gemini API

        Args:
            api_key: Gemini API key (if None, reads from GEMINI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        # Configure Gemini
        genai.configure(api_key=self.api_key)

        # ✅ Using Gemini 2.5 Flash (Latest Stable - June 2025)
        # Supports up to 1 million tokens
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        print("✅ AI Analyzer initialized with gemini-2.5-flash")

    def analyze_issue(self, title: str, description: str, labels: List[str]) -> Dict:
        """
        Analyze a GitHub issue and extract relevant information

        Args:
            title: Issue title
            description: Issue description/body
            labels: List of issue labels

        Returns:
            Dictionary with analysis results
        """
        prompt = self._create_analysis_prompt(title, description, labels)

        try:
            print("🤖 Sending request to Gemini 2.5 Flash AI...")
            response = self.model.generate_content(prompt)
            print("✅ Response received from Gemini 2.5!")
            return self._parse_response(response.text)

        except google_exceptions.NotFound as e:
            return {
                'error': 'Model not found',
                'message': str(e),
                'solution': 'Verify gemini-2.5-flash is available in your region'
            }
        except google_exceptions.InvalidArgument as e:
            return {
                'error': 'Invalid API request',
                'message': str(e)
            }
        except google_exceptions.PermissionDenied as e:
            return {
                'error': 'Permission denied',
                'message': 'Check your API key permissions',
                'details': str(e)
            }
        except google_exceptions.ResourceExhausted as e:
            return {
                'error': 'API quota exceeded',
                'message': 'Rate limit reached. Wait a moment and try again.',
                'details': str(e)
            }
        except google_exceptions.GoogleAPIError as e:
            return {
                'error': 'API Error',
                'message': str(e)
            }

    def _create_analysis_prompt(self, title: str, description: str, labels: List[str]) -> str:
        """Create structured prompt for Gemini 2.5 Flash AI"""
        labels_str = ', '.join(labels) if labels else 'No labels'

        return f"""
You are an expert at analyzing GitHub issues for open-source projects, specifically for Google Summer of Code (GSOC) programs.

Analyze this GitHub issue and provide a structured assessment:

**Issue Title:** {title}

**Description:**
{description}

**Labels:** {labels_str}

Provide a detailed analysis with the following information:

1. **Difficulty Level**: Classify as Beginner, Intermediate, or Advanced
2. **Required Skills**: List all technical skills needed (comma-separated)
3. **Estimated Time**: Provide time in hours (just the number, e.g., "3" or "8-10")
4. **GSOC Friendly**: Answer Yes or No with brief justification
5. **Category**: Classify as bug, feature, documentation, refactoring, enhancement, or testing
6. **Priority**: Rate as Low, Medium, or High
7. **Reasoning**: Provide a concise explanation (1-2 sentences)

Format your response EXACTLY as shown below:
DIFFICULTY: <Beginner|Intermediate|Advanced>
SKILLS: <skill1>, <skill2>, <skill3>
TIME: <number or range>
GSOC_FRIENDLY: <Yes|No>
CATEGORY: <bug|feature|documentation|refactoring|enhancement|testing>
PRIORITY: <Low|Medium|High>
REASONING: <brief explanation>
"""

    def _parse_response(self, response_text: str) -> Dict:
        """Parse AI response into structured data"""
        result = {
            'difficulty': 'Unknown',
            'skills': [],
            'estimated_time': 'Unknown',
            'gsoc_friendly': 'Unknown',
            'category': 'Unknown',
            'priority': 'Unknown',
            'reasoning': '',
            'raw_response': response_text
        }

        try:
            lines = response_text.strip().split('\n')

            for line in lines:
                # Skip empty lines
                if not line.strip():
                    continue

                # Look for key-value pairs
                if ':' not in line:
                    continue

                key, value = line.split(':', 1)
                key = key.strip().upper()
                value = value.strip()

                # Map to result dictionary
                if 'DIFFICULTY' in key:
                    result['difficulty'] = value
                elif 'SKILLS' in key:
                    # Split by comma and clean up
                    result['skills'] = [s.strip() for s in value.split(',') if s.strip()]
                elif 'TIME' in key:
                    result['estimated_time'] = value
                elif 'GSOC' in key or 'FRIENDLY' in key:
                    result['gsoc_friendly'] = value
                elif 'CATEGORY' in key:
                    result['category'] = value
                elif 'PRIORITY' in key:
                    result['priority'] = value
                elif 'REASONING' in key or 'REASON' in key:
                    result['reasoning'] = value

        except ValueError as e:
            result['parse_error'] = f"Failed to parse: {str(e)}"

        return result

    def batch_analyze(self, issues: List[Dict]) -> List[Dict]:
        """
        Analyze multiple issues in batch

        Args:
            issues: List of dictionaries with 'title', 'description', 'labels'

        Returns:
            List of analysis results
        """
        results = []
        total = len(issues)

        print(f"\n🔄 Starting batch analysis of {total} issues...")

        for idx, issue in enumerate(issues, 1):
            print(f"\n{'='*60}")
            print(f"📊 Analyzing issue {idx}/{total}")
            print(f"{'='*60}")

            analysis = self.analyze_issue(
                issue.get('title', 'No title'),
                issue.get('description', 'No description'),
                issue.get('labels', [])
            )

            # Add metadata
            analysis['issue_number'] = idx
            analysis['issue_title'] = issue.get('title')
            results.append(analysis)

        print(f"\n✅ Batch analysis complete! Processed {total} issues.")
        return results


# For testing the module directly
if __name__ == "__main__":
    print("="*60)
    print("🤖 AI Analyzer Module - Gemini 2.5 Flash")
    print("="*60)
    print("✅ Module loaded successfully")
    print("📌 Model: gemini-2.5-flash")
    print("📅 Released: June 2025")
    print("🚀 Context Window: Up to 1 million tokens")
    print("="*60)
