from fastapi import APIRouter, HTTPException, Depends
from app.models.alert import Alert, AlertResponse
from app.utils.gemini_integration import classify_alert_with_gemini
from app.utils.jira_integration import create_jira_ticket
from app.utils.slack_integration import send_slack_alert
import os
from datetime import datetime
import uuid

router = APIRouter()

@router.post("/process_alert", response_model=AlertResponse)
async def process_alert(alert: Alert):
    """
    Process incoming security alerts:
    1. Classify severity using Gemini API
    2. Create JIRA ticket for high/critical alerts
    3. Send Slack notification
    """
    try:
        # Generate unique ID for the alert
        alert_id = str(uuid.uuid4())
        
        # Classify alert severity if not provided
        if not alert.severity:
            severity = await classify_alert_with_gemini(alert.dict())
            alert.severity = severity
        
        # Process high/critical alerts
        if alert.severity in ["Critical", "High"]:
            # Create JIRA ticket
            ticket_id = create_jira_ticket(
                summary=f"Security Alert: {alert.severity} - {alert.source}",
                description=f"""
                Message: {alert.message}
                Source: {alert.source}
                Time: {alert.timestamp}
                Additional Info: {alert.additional_info or 'None'}
                """,
                alert_severity=alert.severity
            )
            
            # Send Slack notification
            send_slack_alert(
                message=f"*{alert.severity} Alert* from {alert.source}: {alert.message}",
                alert=alert.dict()
            )
            
            return AlertResponse(
                status="processed", 
                alert_id=alert_id,
                ticket_id=ticket_id,
                message=f"{alert.severity} alert processed, JIRA ticket created"
            )
        
        # For medium/low alerts, just log
        return AlertResponse(
            status="logged", 
            alert_id=alert_id,
            message=f"{alert.severity} alert logged"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing alert: {str(e)}")

@router.get("/alerts/{alert_id}")
async def get_alert(alert_id: str):
    """
    Get alert details by ID
    Note: In a real implementation, this would fetch from a database
    """
    # This is a placeholder - in a real implementation, you would fetch from a database
    return {"message": "Alert details would be fetched here", "alert_id": alert_id}
