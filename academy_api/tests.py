from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Category, Program, SubscriptionPlan

User = get_user_model()


class ApiSmokeTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user@example.com', email='user@example.com', password='StrongPass123')
        self.token = Token.objects.create(user=self.user)
        self.category = Category.objects.create(name='Entrepreneuriat', slug='entrepreneuriat')
        self.program = Program.objects.create(
            category=self.category,
            title='Lancer son entreprise en Afrique',
            slug='lancer-son-entreprise-en-afrique',
            short_description='Programme MVP',
            description='Description',
            is_published=True,
        )
        self.plan = SubscriptionPlan.objects.create(name='Mensuel', code='mensuel', amount='29.99')

    def test_public_catalog_and_healthcheck(self):
        self.assertEqual(self.client.get('/api/v1/system/health/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get('/api/v1/programs/').status_code, status.HTTP_200_OK)

    def test_authenticated_enrollment(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        response = self.client.post('/api/v1/enrollments/', {'program_id': self.program.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_endpoint(self):
        response = self.client.post(
            reverse('auth-register'),
            {
                'first_name': 'Awa',
                'last_name': 'Diallo',
                'email': 'awa@example.com',
                'password': 'StrongPass123',
            },
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
