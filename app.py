"""
GSOC Buddy AI - Main Application
A Streamlit-based AI agent to help students prepare for Google Summer of Code.

This application helps students:
- Find suitable GitHub issues from GSOC organizations
- Get personalized learning roadmaps
- Track their progress and GitHub contributions
"""

from datetime import datetime
from typing import List, Dict, Any, Optional
import streamlit as st
import requests
from utils.ai_analyzer import AIAnalyzer
import os
import json

def add_n8n_workflow_to_app():
    # Define the path to the n8n workflow JSON file
    workflow_path = "GSOC Issue Fetcher.json"
    
    # Check if the file exists
    if not os.path.exists(workflow_path):
        print(f"Error: Workflow file '{workflow_path}' not found.")
        return False
    
    # Load the workflow JSON
    try:
        with open(workflow_path, 'r') as file:
            workflow_data = json.load(file)
        
        # Here you can integrate the workflow data with your app
        # For example, you might want to:
        # - Store it in a database
        # - Use it to configure routes
        # - Parse it for specific nodes or actions
        
        print(f"Successfully loaded workflow: {workflow_data.get('name', 'Unnamed workflow')}")
        return workflow_data
    
    except json.JSONDecodeError:
        print(f"Error: '{workflow_path}' contains invalid JSON.")
        return False
    except Exception as e:
        print(f"Error loading workflow: {str(e)}")
        return False

# Example usage in your app.py
if __name__ == "__main__":
    # Your existing app code...
    
    # Add the n8n workflow
    workflow = add_n8n_workflow_to_app()
    
    if workflow:
        # Do something with the workflow data
        print(f"Workflow has {len(workflow.get('nodes', []))} nodes")
    
    # Continue with your app...

# Constants
APP_TITLE = "GSOC Buddy AI"
APP_ICON = "🎯"
GITHUB_API_BASE = "https://api.github.com"
DEFAULT_ORG = "omegaup"


def configure_page() -> None:
    """Configure Streamlit page settings and custom CSS."""
    st.set_page_config(
        page_title="My Awesome AI Agent",
        page_icon=APP_ICON,
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        .main-header {
            font-size: 3rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .sub-header {
            font-size: 1.5rem;
            color: #666;
            text-align: center;
            margin-bottom: 3rem;
        }
        </style>
    """, unsafe_allow_html=True)


def render_header() -> None:
    """Render the main application header."""
    st.markdown(
        f'<h1 class="main-header">{APP_ICON} {APP_TITLE}</h1>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<p class="sub-header">'
        'Your AI-Powered Guide to Google Summer of Code Success'
        '</p>',
        unsafe_allow_html=True
    )


def render_feature_cards() -> None:
    """Render the three main feature cards."""
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🔍 Issue Finder")
        st.write(
            "Discover GitHub issues matching your skill level "
            "from GSOC organizations"
        )
        if st.button("Find Issues", key="find_issues"):
            st.info("🚧 Coming soon in Phase 2! We'll build this together.")

    with col2:
        st.markdown("### 🗺️ Learning Roadmap")
        st.write("Get personalized learning paths to solve specific issues")
        if st.button("Create Roadmap", key="roadmap"):
            st.info("🚧 Coming soon in Phase 3! We'll build this together.")

    with col3:
        st.markdown("### 📊 Progress Tracker")
        st.write(
            "Track your GitHub contributions and GSOC preparation progress"
        )
        if st.button("View Progress", key="progress"):
            st.info("🚧 Coming soon in Phase 4! We'll build this together.")


def render_welcome_section() -> None:
    """Render the welcome and about section."""
    st.divider()
    st.markdown("## 👋 Welcome to Your GSOC Journey!")

    st.markdown("""
This AI-powered application helps you prepare for
**Google Summer of Code (GSOC)** by:

1. **Analyzing GitHub Issues** - We scan GSOC organizations
   for beginner-friendly issues
2. **Skill Matching** - AI recommends issues that match your current abilities
3. **Learning Roadmaps** - Get step-by-step guides to solve each issue
4. **Resource Curation** - YouTube tutorials, documentation,
   and courses tailored to you
5. **Progress Tracking** - Monitor your growth and GitHub profile improvement

### 🚀 Getting Started

Use the sidebar to navigate between different features as we build them together!
""")


def render_sidebar() -> None:
    """Render the sidebar with settings."""
    with st.sidebar:
        st.markdown("## ⚙️ Settings")

        # User skill level
        skill_level = st.selectbox(
            "Your Programming Level",
            ["Beginner", "Intermediate", "Advanced"],
            index=0
        )

        # Programming languages
        st.markdown("### Languages You Know")
        python_selected = st.checkbox("Python", value=True)
        javascript_selected = st.checkbox("JavaScript", value=False)
        java_selected = st.checkbox("Java", value=False)
        cpp_selected = st.checkbox("C++", value=False)

        # GitHub username
        github_username = st.text_input("Your GitHub Username (optional)")

        # Save settings button
        if st.button("💾 Save Settings"):
            # Display current settings when saved
            st.success("✅ Settings saved!")
            st.info(f"Skill Level: {skill_level}")
            if github_username:
                st.info(f"GitHub: @{github_username}")

            # Show selected languages
            selected_langs = []
            if python_selected:
                selected_langs.append("Python")
            if javascript_selected:
                selected_langs.append("JavaScript")
            if java_selected:
                selected_langs.append("Java")
            if cpp_selected:
                selected_langs.append("C++")

            if selected_langs:
                st.info(f"Languages: {', '.join(selected_langs)}")

        st.divider()

        # Stats (placeholder for now)
        st.markdown("### 📊 Your Stats")
        st.metric("Issues Analyzed", "0")
        st.metric("Learning Hours", "0")
        st.metric("GitHub Contributions", "0")

        st.divider()

        # Info
        st.markdown("### ℹ️ About")
        st.info(
            "Built with ❤️ for GSOC aspirants\n\n"
            "Powered by Streamlit, Python, and AI"
        )


def fetch_github_issues(
    org: str,
    repo: str,
    label: str = "good first issue",
    max_issues: int = 5
) -> Optional[List[Dict[str, Any]]]:
    """
    Fetch issues from a GitHub repository.

    Args:
        org: GitHub organization name
        repo: Repository name
        label: Issue label to filter by
        max_issues: Maximum number of issues to fetch

    Returns:
        List of issue dictionaries or None if error occurs
    """
    url = f"{GITHUB_API_BASE}/repos/{org}/{repo}/issues"
    params = {
        "state": "open",
        "labels": label,
        "per_page": max_issues
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as error:
        st.error(f"Error fetching issues: {str(error)}")
        return None


def analyze_issue_with_ai(issue: Dict[str, Any], analyzer: AIAnalyzer) -> Optional[Dict]:
    """
    Analyze a GitHub issue using AIAnalyzer.

    Args:
        issue: Dictionary containing issue data from GitHub API
        analyzer: AIAnalyzer instance

    Returns:
        Analysis result dictionary or None if error occurs
    """
    try:
        title = issue.get('title', '')
        body = issue.get('body', '')
        labels = [label['name'] for label in issue.get('labels', [])]

        analysis = analyzer.analyze_issue(title, body, labels)
        return analysis
    except (ValueError, KeyError, AttributeError) as error:
        st.warning(f"⚠️ Could not analyze issue with AI: {str(error)}")
        return None


def render_issue(issue: Dict[str, Any], analyzer: Optional[AIAnalyzer] = None) -> None:
    """
    Render a single GitHub issue in an expander.

    Args:
        issue: Dictionary containing issue data from GitHub API
        analyzer: Optional AIAnalyzer instance for AI-powered analysis
    """
    title = f"#{issue['number']} - {issue['title']}"

    with st.expander(title):
        st.markdown(f"**URL:** {issue['html_url']}")
        st.markdown(f"**Created:** {issue['created_at'][:10]}")

        # Handle labels
        labels = [label['name'] for label in issue.get('labels', [])]
        if labels:
            st.markdown(f"**Labels:** {', '.join(labels)}")

        # Handle body/description
        st.markdown("**Description:**")
        body = issue.get('body', 'No description provided.')
        if body:
            display_text = (
                body[:300] + "..." if len(body) > 300 else body
            )
            st.write(display_text)
        else:
            st.write("No description provided.")

        # AI Analysis (if analyzer available)
        if analyzer:
            if st.button("🤖 Analyze with AI", key=f"analyze_{issue['number']}"):
                with st.spinner("Analyzing issue with AI..."):
                    analysis = analyze_issue_with_ai(issue, analyzer)
                    if analysis:
                        st.success("✅ AI Analysis Complete")
                        st.json(analysis)


def render_github_demo() -> None:
    """Render the GitHub API demo section with AI analysis."""
    st.divider()
    st.markdown("## 🔬 AI-Powered Issue Analysis")
    st.markdown(
        "Fetch GitHub issues and see AI-powered analysis! "
        "The AI will determine difficulty, required skills, and match score."
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        demo_org = st.text_input(
            "GitHub Organization",
            value=DEFAULT_ORG,
            help="Try: omegaup, tensorflow, django, scikit-learn"
        )

    with col2:
        max_issues = st.number_input(
            "Max Issues",
            min_value=1,
            max_value=10,
            value=3,
            help="Number of issues to fetch"
        )

    # Get user preferences from session state (if available)
    if 'user_skills' not in st.session_state:
        st.session_state.user_skills = ["Python"]
    if 'user_level' not in st.session_state:
        st.session_state.user_level = "Beginner"

    if st.button("🤖 Analyze Issues with AI"):
        if not demo_org.strip():
            st.warning("⚠️ Please enter an organization name.")
            return

        with st.spinner("Fetching issues and analyzing with AI..."):
            # Fetch issues
            issues = fetch_github_issues(demo_org, demo_org, max_issues=max_issues)

            if issues is not None and len(issues) > 0:
                st.success(f"✅ Found {len(issues)} issues! Analyzing with AI...")

                # Initialize AI analyzer
                try:
                    analyzer = AIAnalyzer()

                    # Analyze each issue
                    for idx, issue in enumerate(issues, 1):
                        st.markdown(f"### Issue #{idx}: {issue['title']}")

                        # Create columns for issue details and AI analysis
                        col_left, col_right = st.columns([1, 1])

                        with col_left:
                            st.markdown("**📋 Issue Details**")
                            st.markdown(f"**Number:** #{issue['number']}")
                            st.markdown(f"**URL:** [View on GitHub]({issue['html_url']})")
                            st.markdown(f"**Created:** {issue['created_at'][:10]}")

                            labels = [label['name'] for label in issue.get('labels', [])]
                            if labels:
                                st.markdown(f"**Labels:** {', '.join(labels[:3])}")

                            # Show description
                            body = issue.get('body', 'No description')
                            if body:
                                with st.expander("📝 Description"):
                                    st.write(body[:300] + "..." if len(body) > 300 else body)

                        with col_right:
                            st.markdown("**🤖 AI Analysis**")

                            # Analyze with AI
                            with st.spinner("Analyzing..."):
                                analysis = analyzer.analyze_issue(
                                    title=issue['title'],
                                    description=issue.get('body', ''),
                                    labels=labels
                                )

                            # Display analysis
                            difficulty = analysis.get('difficulty', 'unknown')
                            difficulty_color = {
                                'beginner': '🟢',
                                'intermediate': '🟡',
                                'advanced': '🔴'
                            }.get(difficulty, '⚪')

                            st.markdown(f"**Difficulty:** {difficulty_color} {difficulty.title()}")

                            skills = analysis.get('skills_required', [])
                            if skills:
                                st.markdown(f"**Skills:** {', '.join(skills[:4])}")

                            time_est = analysis.get('estimated_hours', 'Unknown')
                            st.markdown(f"**Time:** {time_est}")

                        st.divider()

                except (ValueError, KeyError, AttributeError, RuntimeError) as error:
                    st.error(f"AI Analysis Error: {str(error)}")
                    st.info("Showing issues without AI analysis...")
                    for issue in issues:
                        render_issue(issue)

            elif issues is not None:
                st.warning(
                    f"No 'good first issue' found in {demo_org}/{demo_org}. "
                    "Try another organization!"
                )

    demo_org = st.text_input(
        "Enter a GitHub organization (try: 'omegaup', 'tensorflow', 'django')",
        value=DEFAULT_ORG
    )

    if st.button("🔍 Fetch Sample Issues"):
        if not demo_org.strip():
            st.warning("⚠️ Please enter an organization name.")
            return

        with st.spinner("Fetching issues from GitHub..."):
            # Try organization/organization format first (common pattern)
            issues = fetch_github_issues(demo_org, demo_org)

            if issues is not None:
                if len(issues) > 0:
                    st.success(
                        f"✅ Found {len(issues)} beginner-friendly issues!"
                    )

                    # Initialize AI Analyzer for issue analysis
                    try:
                        analyzer = AIAnalyzer()
                    except ValueError:
                        st.warning("⚠️ GEMINI_API_KEY not set. AI analysis unavailable.")
                        analyzer = None

                    for issue in issues:
                        render_issue(issue, analyzer)
                else:
                    st.warning(
                        f"No 'good first issue' found in {demo_org}/{demo_org}. "
                        "Try another organization or check if the repository exists!"
                    )


def render_footer() -> None:
    """Render the application footer."""
    st.divider()
    current_date = datetime.now().strftime("%B %d, %Y")
    st.markdown(f"""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>{APP_ICON} {APP_TITLE} - Version 0.1.0</p>
    <p>Built during your AI Agent learning journey</p>
    <p>Current Date: {current_date}</p>
</div>
""", unsafe_allow_html=True)


def main() -> None:
    """Main application entry point."""
    # Configure page
    configure_page()

    # Render header
    render_header()

    # Render feature cards
    render_feature_cards()

    # Render welcome section
    render_welcome_section()

    # Render sidebar
    render_sidebar()

    # Render GitHub API demo
    render_github_demo()

    # Render footer
    render_footer()


if __name__ == "__main__":
    main()
