# routes/invoice.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_session
from schemas.invoice_schema import InvoiceCreateSchema
from services.invoice_service import create_invoice_service

router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)


@router.post("/")
async def create_invoice(
    payload: InvoiceCreateSchema,
    db: AsyncSession = Depends(get_session)
):

    return await create_invoice_service(payload, db)