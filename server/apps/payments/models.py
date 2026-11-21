from decimal import Decimal
from django.conf import settings
from django.db import models, transaction
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from apps.job.models import Job

class InvoiceStatus(models.TextChoices):
    ISSUED = "issued", "Issued"
    PARTIALLY_PAID = "partially_paid", "Partially Paid"
    PAID = "paid", "Paid"

class PaymentMethod(models.TextChoices):
    CASH = "cash", "Cash"
    CARD = "card", "Card"
    BANK_TRANSFER = "bank_transfer", "Bank Transfer"
    MOBILE_WALLET = "mobile_wallet", "Mobile Wallet"

class Invoice(models.Model):
    job = models.OneToOneField(Job, on_delete = models.PROTECT, related_name = 'invoice')
    invoice_number = models.CharField(max_length = 30, unique = True, editable = False, blank = True)
    status = models.CharField(max_length = 20, choices = InvoiceStatus.choices, default = InvoiceStatus.ISSUED)
    parts_total = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0, validators = [MinValueValidator(0)])
    labor_total = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0, validators = [MinValueValidator(0)])
    subtotal = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0, validators = [MinValueValidator(0)])
    discount = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0, validators = [MinValueValidator(0)])
    tax_percent = models.DecimalField(max_digits = 5, decimal_places = 2, default = 0, validators = [MinValueValidator(0), MaxValueValidator(100)])
    tax_amount = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0, validators = [MinValueValidator(0)])
    total = models.DecimalField(max_digits = 12, decimal_places = 2, default = 0, validators = [MinValueValidator(0)])
    issued_at = models.DateTimeField(default = timezone.now)
    due_date = models.DateField(null = True, blank = True)
    paid_at = models.DateTimeField(null = True, blank = True)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'issued_invoices')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.invoice_number:
            self.invoice_number = f"INV-{self.issued_at.year}-{self.pk:06d}"
            type(self).objects.filter(pk = self.pk).update(invoice_number = self.invoice_number)

    # @property
    # def amount_paid(self):
    #     return self.payments.aggregate(total = models.Sum('amount'))['total'] or Decimal('0.00')

    # @property
    # def balance_due(self):
    #     return self.total - self.amount_paid

    def __str__(self):
        return self.invoice_number

    class Meta:
        ordering = ['-issued_at', '-id']
        # payments = None

class Payment(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete = models.PROTECT, related_name = 'payments')
    receipt_number = models.CharField(max_length = 30, unique = True, editable = False, blank = True)
    amount = models.DecimalField(max_digits = 12, decimal_places = 2, validators = [MinValueValidator(Decimal('0.01'))])
    method = models.CharField(max_length = 20, choices = PaymentMethod.choices)
    reference = models.CharField(max_length = 100, blank = True)
    paid_at = models.DateTimeField(default = timezone.now)
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.PROTECT, related_name = 'received_payments')
    created_at = models.DateTimeField(auto_now_add = True)

    @transaction.atomic
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new and not self.receipt_number:
            self.receipt_number = f"REC-{self.paid_at.year}-{self.pk:06d}"
            type(self).objects.filter(pk = self.pk).update(receipt_number = self.receipt_number)

    def __str__(self):
        return self.receipt_number

    class Meta:
        ordering = ['-paid_at', '-id']
