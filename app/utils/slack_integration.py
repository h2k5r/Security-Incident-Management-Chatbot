from slack_sdk.webhook import WebhookClient
import os
from dotenv import load_dotenv
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Slack Configuration
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def send_slack_alert(message, alert):
    """
    Send alert notifications to Slack channel
    """
    try:
        webhook = WebhookClient(SLACK_WEBHOOK_URL)
        
        # Determine color based on severity
        color_map = {
            "Critical": "#FF0000",  # Red
            "High": "#FFA500",      # Orange
            "Medium": "#FFFF00",    # Yellow
            "Low": "#00FF00"        # Green
        }
        
        color = color_map.get(alert.get("severity", "Medium"), "#FFFF00")
        
        # Create a formatted message
        payload = {
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🚨 Security Alert 🚨"
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"*Source*: {alert.get('source')} | *Time*: {alert.get('timestamp')}"
                        }
                    ]
                }
            ],
            "attachments": [
                {
                    "color": color,
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*Severity*: {alert.get('severity', 'Unknown')}"
                            }
                        }
                    ]
                }
            ]
        }
        
        # Send the message
        response = webhook.send_dict(payload)
        return response.status_code
        
    except Exception as e:
        print(f"Error sending Slack alert: {str(e)}")
        return None
