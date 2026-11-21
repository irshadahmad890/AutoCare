from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from apps.customers.models import Customer
from apps.job.models import EstimateStatus, Job, JobMechanic, JobPart, JobStatus
from apps.mechanics.models import Mechanic, Specialization
from apps.parts.models import Part
from apps.user.models import Role, User
from apps.vehicle.models import Vehicle


class JobWorkflowTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user('admin', 'admin@example.com', 'pass12345', role=Role.ADMIN)
        self.customer_user = User.objects.create_user('customer', 'customer@example.com', 'pass12345', role=Role.CUSTOMER)
        self.other_customer = User.objects.create_user('other', 'other@example.com', 'pass12345', role=Role.CUSTOMER)
        self.customer = Customer.objects.create(user=self.customer_user, name='Customer')
        self.other = Customer.objects.create(user=self.other_customer, name='Other Customer')
        self.vehicle = Vehicle.objects.create(customer=self.customer, make='Honda', model='Civic', year=2020, registration_number='ABC-123')
        self.job = Job.objects.create(vehicle=self.vehicle, description='Brake repair')
        self.part = Part.objects.create(name='Brake Pad', part_number='BP-1', price=Decimal('50.00'), stock=3)
        self.job_part = JobPart.objects.create(job=self.job, part=self.part, quantity=2, unit_price=self.part.price)
        self.client = APIClient()

    def test_customer_approval_deducts_stock_once(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(f'/jobs/{self.job.pk}/estimate/send/', {'notes': 'Replace pads'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.job.refresh_from_db()
        self.assertEqual(self.job.status, JobStatus.AWAITING_APPROVAL)
        self.part.refresh_from_db()
        self.assertEqual(self.part.stock, 3)

        self.client.force_authenticate(self.customer_user)
        response = self.client.post(f'/jobs/{self.job.pk}/estimate/respond/', {'approve': True}, format='json')
        self.assertEqual(response.status_code, 200)
        self.part.refresh_from_db()
        self.job.refresh_from_db()
        self.assertEqual(self.part.stock, 1)
        self.assertEqual(self.job.status, JobStatus.APPROVED)
        self.assertEqual(self.job.estimate.status, EstimateStatus.APPROVED)

        response = self.client.post(f'/jobs/{self.job.pk}/estimate/respond/', {'approve': True}, format='json')
        self.assertEqual(response.status_code, 400)
        self.part.refresh_from_db()
        self.assertEqual(self.part.stock, 1)

    def test_other_customer_cannot_read_or_approve_job(self):
        self.client.force_authenticate(self.other_customer)
        self.assertEqual(self.client.get(f'/jobs/{self.job.pk}/').status_code, 404)
        self.assertEqual(
            self.client.post(f'/jobs/{self.job.pk}/estimate/respond/', {'approve': True}, format='json').status_code,
            400,
        )

    def test_assigned_mechanic_can_progress_but_not_edit_customer_job(self):
        mechanic_user = User.objects.create_user('mechanic', 'mechanic@example.com', 'pass12345', role=Role.MECHANIC)
        specialization = Specialization.objects.create(name='General')
        mechanic = Mechanic.objects.create(user=mechanic_user, specialization=specialization, name='Mechanic', experience_level='senior', hourly_rate=Decimal('20'))
        JobMechanic.objects.create(job=self.job, mechanic=mechanic)
        self.client.force_authenticate(self.admin)
        self.client.post(f'/jobs/{self.job.pk}/estimate/send/', {}, format='json')
        self.client.force_authenticate(self.customer_user)
        self.client.post(f'/jobs/{self.job.pk}/estimate/respond/', {'approve': True}, format='json')

        self.client.force_authenticate(mechanic_user)
        response = self.client.post(f'/jobs/{self.job.pk}/transition/', {'status': JobStatus.IN_PROGRESS}, format='json')
        self.assertEqual(response.status_code, 200)
        response = self.client.patch(f'/jobs/{self.job.pk}/', {'description': 'Changed'}, format='json')
        self.assertEqual(response.status_code, 403)
