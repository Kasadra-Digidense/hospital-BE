# app/services/invoice_service.py

from models.invoice import Invoice
from models.invoice_room_charge import InvoiceRoomCharge
from models.invoice_treatment_charge import InvoiceTreatmentCharge
from models.invoice_additional_charges          import InvoiceAdditionalCharge
from models.invoice_payment import InvoicePayment


def create_invoice_service(payload, db):

    try:

        # -----------------------------
        # CALCULATE TOTALS
        # -----------------------------

        room_total = sum(
            item.amount for item in payload.room_charges
        )

        treatment_total = sum(
            item.amount for item in payload.treatment_charges
        )

        additional_total = sum(
            item.amount for item in payload.additional_charges
        )

        gross_total = (
            room_total +
            treatment_total +
            additional_total
        )

        paid_total = sum(
            item.amount for item in payload.payments
        )

        balance_total = gross_total - paid_total

        # -----------------------------
        # GENERATE BILL NUMBER
        # -----------------------------

        latest_invoice = (
            db.query(Invoice)
            .order_by(Invoice.id.desc())
            .first()
        )

        next_id = 1

        if latest_invoice:
            next_id = latest_invoice.id + 1

        bill_no = f"INV-2026-{str(next_id).zfill(5)}"

        # -----------------------------
        # CREATE MAIN INVOICE
        # -----------------------------

        invoice = Invoice(
            patient_id=payload.patient_id,

            bill_no=bill_no,

            admission_date=payload.admission_date,
            discharge_date=payload.discharge_date,

            consultant=payload.consultant,

            room_type=payload.room_type,
            room_number=payload.room_number,

            gross_total=gross_total,
            paid_total=paid_total,
            balance_total=balance_total
        )

        db.add(invoice)

        # IMPORTANT
        db.flush()

        # -----------------------------
        # SAVE ROOM CHARGES
        # -----------------------------

        for room in payload.room_charges:

            room_charge = InvoiceRoomCharge(
                invoice_id=invoice.id,

                room_id=room.room_id,

                days=room.days,

                rate=room.rate,

                amount=room.amount
            )

            db.add(room_charge)

        # -----------------------------
        # SAVE TREATMENT CHARGES
        # -----------------------------

        for treatment in payload.treatment_charges:

            treatment_charge = InvoiceTreatmentCharge(
                invoice_id=invoice.id,

                treatment_id=treatment.treatment_id,

                qty=treatment.qty,

                rate=treatment.rate,

                amount=treatment.amount
            )

            db.add(treatment_charge)

        # -----------------------------
        # SAVE ADDITIONAL CHARGES
        # -----------------------------

        for extra in payload.additional_charges:

            additional_charge = InvoiceAdditionalCharge(
                invoice_id=invoice.id,

                charge_type=extra.charge_type,

                amount=extra.amount
            )

            db.add(additional_charge)

        # -----------------------------
        # SAVE PAYMENTS
        # -----------------------------

        for payment in payload.payments:

            invoice_payment = InvoicePayment(
                invoice_id=invoice.id,

                method=payment.method,

                amount=payment.amount
            )

            db.add(invoice_payment)

        # -----------------------------
        # COMMIT EVERYTHING
        # -----------------------------

        db.commit()

        db.refresh(invoice)

        return {
            "success": True,

            "message": "Invoice created successfully",

            "invoice_id": invoice.id,

            "bill_no": invoice.bill_no,

            "gross_total": invoice.gross_total,

            "paid_total": invoice.paid_total,

            "balance_total": invoice.balance_total
        }

    except Exception as e:

        db.rollback()

        raise e