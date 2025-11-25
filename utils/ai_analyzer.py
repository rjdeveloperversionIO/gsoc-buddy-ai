"""
AI Analyzer Module for GSOC Buddy AI.

This module uses Google Gemini AI to analyze GitHub issues and extract:
- Difficulty level
- Required programming skills
- Estimated completion time
- Suitability for GSOC beginners
- Learning resources needed
"""

import os
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import google.generativeai as genai


# Load environment variables
load_dotenv()

# Configure Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class IssueAnalyzer:
    """Analyzes GitHub issues using AI to extract relevant information."""

    def __init__(self, model_name: str = "gemini-pro") -> None:
        """
        Initialize the Issue Analyzer.

        Args:
            model_name: Name of the Gemini model to use
        """
        if not GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "Please add it to your .env file."
            )

        self.model = genai.GenerativeModel(model_name)
        self.analysis_cache: Dict[str, Dict[str, Any]] = {}

    def analyze_issue(
        self,
        title: str,
        description: str,
        labels: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze a GitHub issue using AI.

        Args:
            title: Issue title
            description: Issue description/body
            labels: List of issue labels (optional)

        Returns:
            Dictionary containing analysis results
        """
        # Create cache key
        cache_key = f"{title}:{description[:100]}"

        # Check cache first
        if cache_key in self.analysis_cache:
            return self.analysis_cache[cache_key]

        # Prepare the prompt
        prompt = self._create_analysis_prompt(title, description, labels)

        try:
            # Get AI response
            response = self.model.generate_content(prompt)

            # Parse the response
            analysis = self._parse_ai_response(response.text)

            # Add metadata
            analysis["original_title"] = title
            analysis["original_description"] = description[:200]
            analysis["labels"] = labels or []

            # Cache the result
            self.analysis_cache[cache_key] = analysis

            return analysis

        except (ValueError, AttributeError, TypeError) as error:
            # Return error analysis
            return {
                "error": str(error),
                "difficulty": "unknown",
                "skills_required": [],
                "good_for_beginners": False,
                "original_title": title
            }

    def _create_analysis_prompt(
        self,
        title: str,
        description: str,
        labels: Optional[List[str]]
    ) -> str:
        """
        Create a structured prompt for AI analysis.

        Args:
            title: Issue title
            description: Issue description
            labels: Issue labels

        Returns:
            Formatted prompt string
        """
        label_text = f"Labels: {', '.join(labels)}" if labels else ""

        prompt = f"""
Analyze this GitHub issue and provide structured information:

**Title:** {title}

**Description:** {description}

{label_text}

Please provide analysis in the following format:

DIFFICULTY: [beginner/intermediate/advanced]
SKILLS: [comma-separated list of required skills/technologies]
TIME_ESTIMATE: [estimated hours to complete]
GOOD_FOR_GSOC: [yes/no]
CONCEPTS: [key programming concepts needed]
EXPLANATION: [brief explanation of why this difficulty level]

Be specific and technical. Focus on programming languages and frameworks.
"""
        return prompt

    def _parse_ai_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse AI response into structured data.

        Args:
            response_text: Raw AI response

        Returns:
            Dictionary with parsed data
        """
        # Initialize result
        result: Dict[str, Any] = {
            "difficulty": "unknown",
            "skills_required": [],
            "estimated_hours": "unknown",
            "good_for_beginners": False,
            "concepts_needed": [],
            "explanation": ""
        }

        try:
            # Parse each line
            lines = response_text.strip().split('\n')

            for line in lines:
                line = line.strip()

                if line.startswith("DIFFICULTY:"):
                    difficulty = line.split(":", 1)[1].strip().lower()
                    result["difficulty"] = difficulty
                    result["good_for_beginners"] = difficulty == "beginner"

                elif line.startswith("SKILLS:"):
                    skills_text = line.split(":", 1)[1].strip()
                    skills = [
                        s.strip()
                        for s in skills_text.split(",")
                        if s.strip()
                    ]
                    result["skills_required"] = skills

                elif line.startswith("TIME_ESTIMATE:"):
                    time_est = line.split(":", 1)[1].strip()
                    result["estimated_hours"] = time_est

                elif line.startswith("GOOD_FOR_GSOC:"):
                    gsoc_suitable = line.split(":", 1)[1].strip().lower()
                    result["good_for_gsoc"] = gsoc_suitable == "yes"

                elif line.startswith("CONCEPTS:"):
                    concepts_text = line.split(":", 1)[1].strip()
                    concepts = [
                        c.strip()
                        for c in concepts_text.split(",")
                        if c.strip()
                    ]
                    result["concepts_needed"] = concepts

                elif line.startswith("EXPLANATION:"):
                    explanation = line.split(":", 1)[1].strip()
                    result["explanation"] = explanation

        except (ValueError, IndexError, AttributeError) as error:
            result["parsing_error"] = str(error)

        return result

    def calculate_match_score(
        self,
        issue_analysis: Dict[str, Any],
        user_skills: List[str],
        user_level: str
    ) -> Dict[str, Any]:
        """
        Calculate how well an issue matches a user's profile.

        Args:
            issue_analysis: Analysis result from analyze_issue()
            user_skills: List of user's programming skills
            user_level: User's skill level (beginner/intermediate/advanced)

        Returns:
            Dictionary with match score and explanation
        """
        # Normalize inputs
        user_skills_lower = [s.lower() for s in user_skills]
        required_skills = issue_analysis.get("skills_required", [])
        required_skills_lower = [s.lower() for s in required_skills]

        # Calculate skill match
        if not required_skills_lower:
            skill_match = 0.5  # Unknown requirements = 50%
        else:
            matching_skills = sum(
                1 for skill in required_skills_lower
                if skill in user_skills_lower
            )
            skill_match = matching_skills / len(required_skills_lower)

        # Calculate level match
        issue_difficulty = issue_analysis.get("difficulty", "unknown")
        level_scores = {
            ("beginner", "beginner"): 1.0,
            ("beginner", "intermediate"): 0.8,
            ("beginner", "advanced"): 0.6,
            ("intermediate", "beginner"): 0.5,
            ("intermediate", "intermediate"): 1.0,
            ("intermediate", "advanced"): 0.8,
            ("advanced", "beginner"): 0.3,
            ("advanced", "intermediate"): 0.6,
            ("advanced", "advanced"): 1.0,
        }
        level_match = level_scores.get(
            (issue_difficulty, user_level.lower()),
            0.5
        )

        # Calculate overall match (70% skills, 30% level)
        overall_match = (skill_match * 0.7) + (level_match * 0.3)

        # Generate explanation
        matching_skills_list = [
            skill for skill in required_skills
            if skill.lower() in user_skills_lower
        ]
        missing_skills_list = [
            skill for skill in required_skills
            if skill.lower() not in user_skills_lower
        ]

        explanation_parts = []

        if matching_skills_list:
            explanation_parts.append(
                f"✅ You know: {', '.join(matching_skills_list)}"
            )

        if missing_skills_list:
            explanation_parts.append(
                f"📚 You need to learn: {', '.join(missing_skills_list)}"
            )

        if issue_difficulty != user_level.lower():
            explanation_parts.append(
                f"⚠️ Issue is {issue_difficulty}, "
                f"you're {user_level.lower()}"
            )

        explanation = " | ".join(explanation_parts)

        return {
            "match_percentage": round(overall_match * 100),
            "skill_match": round(skill_match * 100),
            "level_match": round(level_match * 100),
            "explanation": explanation,
            "matching_skills": matching_skills_list,
            "missing_skills": missing_skills_list,
            "recommendation": self._get_recommendation(overall_match)
        }

    def _get_recommendation(self, match_score: float) -> str:
        """
        Get recommendation based on match score.

        Args:
            match_score: Match score (0.0 to 1.0)

        Returns:
            Recommendation string
        """
        if match_score >= 0.8:
            return "🟢 Excellent match! Start working on this."
        elif match_score >= 0.6:
            return "🟡 Good match. Minor learning needed."
        elif match_score >= 0.4:
            return "🟠 Moderate match. Some learning required."
        else:
            return "🔴 Low match. Better to learn more first."


def quick_analyze(title: str, description: str) -> Dict[str, Any]:
    """
    Quick analysis function for simple use cases.

    Args:
        title: Issue title
        description: Issue description

    Returns:
        Analysis dictionary
    """
    analyzer = IssueAnalyzer()
    return analyzer.analyze_issue(title, description)
