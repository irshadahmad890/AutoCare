from decimal import Decimal

from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.job.models import Job, JobStatus
from .models import Invoice, InvoiceStatus, Payment
from .validators import validate_discount, validate_payment_amount


@transaction.atomic
def generate_invoice(job_id, issued_by, discount = Decimal('0.00'), tax_percent = Decimal('0.00')):

    job = Job.objects.select_for_update().get(pk = job_id)

    if job.status != JobStatus.COMPLETED:
        raise ValidationError("Invoice can only be generated for completed jobs.")

    if hasattr(job, 'invoice'):
        raise ValidationError("An invoice already exists for this job.")

    parts_total = sum(
        (item.quantity * item.unit_price for item in job.used_parts.all()),
        Decimal('0.00')
    )

    labor_total = sum(
        (assignment.working_hours * assignment.mechanic.hourly_rate
         for assignment in job.mechanic_assignments.select_related('mechanic')),
        Decimal('0.00')
    )

    subtotal = parts_total + labor_total

    validate_discount(discount, subtotal)

    taxable_amount = subtotal - discount
    tax_amount = (taxable_amount * tax_percent / Decimal('100')).quantize(Decimal('0.01'))
    total = taxable_amount + tax_amount

    return Invoice.objects.create(
        job = job,
        parts_total = parts_total,
        labor_total = labor_total,
        subtotal = subtotal,
        discount = discount,
        tax_percent = tax_percent,
        tax_amount = tax_amount,
        total = total,
        issued_by = issued_by
    )


@transaction.atomic
def record_payment(invoice_id, amount, method, reference, received_by):

    invoice = Invoice.objects.select_for_update().get(pk = invoice_id)

    validate_payment_amount(amount, invoice.balance_due)

    payment = Payment.objects.create(
        invoice = invoice,
        amount = amount,
        method = method,
        reference = reference,
        received_by = received_by
    )

    invoice.refresh_from_db()

    if invoice.balance_due <= 0:
        invoice.status = InvoiceStatus.PAID
        invoice.paid_at = timezone.now()

    elif invoice.amount_paid > 0:
        invoice.status = InvoiceStatus.PARTIALLY_PAID

    else:
        invoice.status = InvoiceStatus.ISSUED

    invoice.save(update_fields = ['status', 'paid_at', 'updated_at'])

    return payment
