import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

async def classify_alert_with_gemini(alert_data):
    """
    Use Gemini API to classify the severity of a security alert
    """
    try:
        headers = {"Content-Type": "application/json"}
        params = {"key": GEMINI_API_KEY}
        
        # Create prompt for Gemini
        prompt = f"""
        Classify this security alert into exactly one of these categories: Critical, High, Medium, or Low.
        Only respond with the category name, nothing else.
        
        Source: {alert_data['source']}
        Message: {alert_data['message']}
        Timestamp: {alert_data['timestamp']}
        """
        
        # Make request to Gemini API
        response = requests.post(
            GEMINI_URL,
            headers=headers,
            params=params,
            json={"contents": [{"parts": [{"text": prompt}]}]}
        )
        
        # Parse response
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            severity = result['candidates'][0]['content']['parts'][0]['text'].strip()
            # Ensure it's one of our expected values
            if severity in ["Critical", "High", "Medium", "Low"]:
                return severity
            else:
                return "Medium"  # Default if classification is unexpected
        else:
            return "Medium"  # Default if API fails
            
    except Exception as e:
        print(f"Error classifying alert with Gemini: {str(e)}")
        return "Medium"  # Default to Medium if there's an error
