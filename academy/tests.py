from django.test import TestCase
from django.urls import reverse


class AcademyPageTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('academy:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Solu Africa Academy')

    def test_courses_page(self):
        response = self.client.get(reverse('academy:courses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nos formations')

    def test_auth_page(self):
        response = self.client.get(reverse('academy:auth'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Connexion apprenant')

    def test_dashboard_page(self):
        response = self.client.get(reverse('academy:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tableau de bord')
