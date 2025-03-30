from pydantic import BaseModel, Field
from typing import Optional, Dict
from datetime import datetime
from enum import Enum

class SeverityLevel(str, Enum):
    critical = "Critical"
    high = "High"
    medium = "Medium"
    low = "Low"

class Alert(BaseModel):
    source: str = Field(..., description="Source of the alert")
    message: str = Field(..., description="Alert message")
    timestamp: datetime = Field(default_factory=datetime.now, description="Time of the alert")
    severity: Optional[SeverityLevel] = None
    additional_info: Optional[Dict] = None
    
class AlertResponse(BaseModel):
    status: str
    alert_id: Optional[str] = None
    ticket_id: Optional[str] = None
    message: Optional[str] = None
