from decimal import Decimal

from django.test import TestCase

from apps.customers.models import Customer
from apps.job.models import Estimate, EstimateStatus, Job, JobStatus
from apps.parts.models import Part
from apps.user.models import Role, User
from apps.vehicle.models import Vehicle
from .models import Invoice, InvoiceStatus, PaymentMethod
from .services import record_payment


class PaymentServiceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin', 'admin@example.com', 'pass12345', role=Role.ADMIN)
        customer_user = User.objects.create_user('customer', 'customer@example.com', 'pass12345', role=Role.CUSTOMER)
        customer = Customer.objects.create(user=customer_user, name='Customer')
        vehicle = Vehicle.objects.create(customer=customer, make='Toyota', model='Yaris', year=2020, registration_number='PAY-1')
        job = Job.objects.create(vehicle=vehicle, status=JobStatus.COMPLETED)
        Estimate.objects.create(job=job, status=EstimateStatus.APPROVED, stock_deducted=True, approved_by=customer_user)
        self.invoice = Invoice.objects.create(job=job, issued_by=self.admin, total=Decimal('100.00'))

    def test_payment_updates_invoice_status_and_prevents_overpayment(self):
        record_payment(self.invoice.pk, Decimal('40.00'), PaymentMethod.CASH, '', self.admin)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, InvoiceStatus.PARTIALLY_PAID)
        record_payment(self.invoice.pk, Decimal('60.00'), PaymentMethod.CARD, 'ref', self.admin)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.status, InvoiceStatus.PAID)
        self.assertEqual(self.invoice.balance_due, Decimal('0.00'))
