from django.test import TestCase
from rest_framework.test import APIClient

from apps.mechanics.models import Mechanic, Specialization
from apps.user.models import Role, User
from .models import Part


class MechanicInventoryAccessTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(
            'mechanic', 'mechanic@example.com', 'pass12345', role=Role.MECHANIC
        )
        specialization = Specialization.objects.create(name='Engine')
        Mechanic.objects.create(
            user=user, specialization=specialization, name='Mechanic',
            experience_level='junior', hourly_rate=10,
        )
        Part.objects.create(name='Oil filter', part_number='OF-1', price=10, stock=3)
        self.client = APIClient()
        self.client.force_authenticate(user)

    def test_mechanic_can_read_but_not_change_parts_catalog(self):
        self.assertEqual(self.client.get('/parts/').status_code, 200)
        response = self.client.post('/parts/', {
            'name': 'Spark plug', 'part_number': 'SP-1', 'price': '5.00', 'stock': 2,
        }, format='json')
        self.assertEqual(response.status_code, 403)
