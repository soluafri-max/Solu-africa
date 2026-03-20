from django.test import SimpleTestCase
from django.urls import reverse


class FrontendPagesTests(SimpleTestCase):
    def test_pages_return_success(self):
        urls = [
            reverse('home'),
            reverse('catalogue'),
            reverse('dashboard'),
            reverse('program_detail', kwargs={'slug': 'lancer-son-entreprise-en-afrique'}),
            reverse('lesson_player', kwargs={'slug': 'lancer-son-entreprise-en-afrique'}),
            reverse('community'),
            reverse('admin_overview'),
        ]

        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)
