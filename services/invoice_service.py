# app/services/invoice_service.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from models.invoice import Invoice
from models.invoice_room_charge import InvoiceRoomCharge
from models.invoice_treatment_charge import InvoiceTreatmentCharge
from models.invoice_additional_charges import InvoiceAdditionalCharge
from models.invoice_payment import InvoicePayment
from models.patient import Patient


async def create_invoice_service(payload, db: AsyncSession):

    try:

        # =========================
        # CHECK PATIENT EXISTS
        # =========================
        patient_result = await db.execute(
            select(Patient).where(Patient.id == payload.patient_id)
        )

        patient = patient_result.scalar_one_or_none()

        if not patient:
            return {
                "success": False,
                "message": "Patient not found"
            }

        # =========================
        # GENERATE BILL NUMBER
        # =========================
        last_invoice_result = await db.execute(
            select(Invoice).order_by(desc(Invoice.id)).limit(1)
        )

        last_invoice = last_invoice_result.scalar_one_or_none()

        if last_invoice:
            next_id = last_invoice.id + 1
        else:
            next_id = 1

        bill_no = f"INV-{next_id:05d}"

        # =========================
        # CREATE MAIN INVOICE
        # =========================
        invoice = Invoice(
            patient_id=payload.patient_id,

            admission_date=payload.admission_date,
            discharge_date=payload.discharge_date,

            consultant=payload.consultant,

            room_type=payload.room_type,
            room_number=payload.room_number,

            bill_no=bill_no,

            room_total=payload.room_total,
            treatment_total=payload.treatment_total,
            extra_total=payload.extra_total,

            gross_total=payload.gross_total,
            total_paid=payload.total_paid,
            balance=payload.balance,
        )

        db.add(invoice)

        await db.commit()
        await db.refresh(invoice)

        # =========================
        # SAVE ROOM CHARGES
        # =========================
        for room in payload.room_charges:

            room_obj = InvoiceRoomCharge(
                invoice_id=invoice.id,

                room_id=room.room_id,

                days=room.days,
                rate=room.rate,
                amount=room.amount,
            )

            db.add(room_obj)

        # =========================
        # SAVE TREATMENT CHARGES
        # =========================
        for treatment in payload.treatment_charges:

            treatment_obj = InvoiceTreatmentCharge(
                invoice_id=invoice.id,

                treatment_id=treatment.treatment_id,

                qty=treatment.qty,
                rate=treatment.rate,
                amount=treatment.amount,
            )

            db.add(treatment_obj)

        # =========================
        # SAVE ADDITIONAL CHARGES
        # =========================
        for charge in payload.additional_charges:

            charge_obj = InvoiceAdditionalCharge(
                invoice_id=invoice.id,

                # charge_type=charge.charge_type,
                charge_type=charge.type,
                amount=charge.amount,
            )

            db.add(charge_obj)

        # =========================
        # SAVE PAYMENTS
        # =========================
        for payment in payload.payments:

            payment_obj = InvoicePayment(
                invoice_id=invoice.id,

                method=payment.method,
                amount=payment.amount,
            )

            db.add(payment_obj)

        await db.commit()

        # =========================
        # SUCCESS RESPONSE
        # =========================
        return {
            "success": True,
            "message": "Invoice created successfully",

            "invoice": {
                "invoice_id": invoice.id,

                "bill_no": invoice.bill_no,

                "patient_id": invoice.patient_id,

                "admission_date": invoice.admission_date,
                "discharge_date": invoice.discharge_date,

                "gross_total": invoice.gross_total,
                "total_paid": invoice.total_paid,
                "balance": invoice.balance,
            }
        }

    except Exception as e:

        await db.rollback()

        return {
            "success": False,
            "detail": str(e)
        }