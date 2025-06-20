from fastapi import APIRouter
from models import Invoice

router = APIRouter()
@router.post("/invoices", tags=["Invoices"])
async def create_invoice(invoice_data: Invoice):
    return {
        "message": "INVOICE created successfully",
        "customer": invoice_data
    }