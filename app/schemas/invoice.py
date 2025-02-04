from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class InvoiceItem(BaseModel):
    description: str
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_amount: Optional[float] = None

class Invoice(BaseModel):
    invoice_number: str
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    company_name: Optional[str] = None
    company_address: Optional[str] = None
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    total_amount: Optional[float] = None
    items: List[InvoiceItem] = []
    currency: Optional[str] = None
    payment_terms: Optional[str] = None
    
    class Config:
        from_attributes = True
