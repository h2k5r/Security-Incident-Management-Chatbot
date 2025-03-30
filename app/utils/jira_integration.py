from jira import JIRA
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JIRA Configuration
JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = "SEC"  # Security project key

def create_jira_ticket(summary, description, alert_severity):
    """
    Create a JIRA ticket for security incidents
    """
    try:
        # Connect to JIRA
        jira = JIRA(server=JIRA_URL, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
        
        # Map alert severity to JIRA priority
        priority_map = {
            "Critical": "Highest",
            "High": "High",
            "Medium": "Medium",
            "Low": "Low"
        }
        
        # Create issue dict
        issue_dict = {
            'project': {'key': JIRA_PROJECT_KEY},
            'summary': summary,
            'description': description,
            'issuetype': {'name': 'Incident'},
            'priority': {'name': priority_map.get(alert_severity, "Medium")}
        }
        
        # Create the issue
        issue = jira.create_issue(fields=issue_dict)
        return issue.key
        
    except Exception as e:
        print(f"Error creating JIRA ticket: {str(e)}")
        return None
