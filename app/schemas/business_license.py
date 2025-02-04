from pydantic import BaseModel
from typing import Optional
from datetime import date

class BusinessLicense(BaseModel):
    business_name: str
    registration_number: Optional[str] = None
    address: Optional[str] = None
    issue_date: Optional[date] = None
    
    class Config:
        from_attributes = True