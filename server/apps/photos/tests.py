from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from apps.customers.models import Customer
from apps.job.models import Job
from apps.mechanics.models import Mechanic, Specialization
from apps.user.models import Role, User
from apps.vehicle.models import Vehicle

class RepairPhotoPermissionTests(TestCase):
    def setUp(self):
        self.customer_user = User.objects.create_user('customer', 'customer@example.com', 'pass12345', role=Role.CUSTOMER)
        customer = Customer.objects.create(user=self.customer_user, name='Customer')
        vehicle = Vehicle.objects.create(customer=customer, make='Ford', model='Focus', year=2019, registration_number='PHOTO-1')
        self.job = Job.objects.create(vehicle=vehicle)
        self.mechanic_user = User.objects.create_user('mechanic', 'mechanic@example.com', 'pass12345', role=Role.MECHANIC)
        specialization = Specialization.objects.create(name='Bodywork')
        mechanic = Mechanic.objects.create(user=self.mechanic_user, specialization=specialization, name='Mechanic', experience_level='junior', hourly_rate=10)
        from apps.job.models import JobMechanic
        JobMechanic.objects.create(job=self.job, mechanic=mechanic)
        self.client = APIClient()

    def test_assigned_mechanic_uploads_and_owner_can_list_photo(self):
        self.client.force_authenticate(self.mechanic_user)
        image = SimpleUploadedFile('progress.jpg', b'\xff\xd8\xff\xe0repair-photo', content_type='image/jpeg')
        response = self.client.post('/photos/', {'job': self.job.pk, 'image': image, 'caption': 'Before'}, format='multipart')
        self.assertEqual(response.status_code, 201)
        self.client.force_authenticate(self.customer_user)
        response = self.client.get('/photos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['count'], 1)
