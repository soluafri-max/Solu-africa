import json

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Course, Enrollment, Lesson, LessonProgress, Module, StudentProfile

User = get_user_model()


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


class AcademyApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = 'StrongPass123!'
        self.user = User.objects.create_user(username='amina', email='amina@example.com', password=self.password)
        self.profile = StudentProfile.objects.create(user=self.user, country='Cameroun', job_title='Développeuse junior')
        self.course = Course.objects.create(
            title='Python pour débutants',
            slug='python-pour-debutants',
            short_description='Apprenez les bases de Python.',
            description='Un cours complet pour prendre en main Python.',
            level=Course.BEGINNER,
            duration_weeks=6,
        )
        self.module = Module.objects.create(course=self.course, title='Fondamentaux', summary='Variables et structures de contrôle', order=1)
        self.lesson = Lesson.objects.create(
            module=self.module,
            title='Variables et types',
            slug='variables-et-types',
            content='Contenu de la leçon',
            duration_minutes=20,
            order=1,
            is_preview=True,
        )

    def test_health_endpoint(self):
        response = self.client.get(reverse('academy:api-health'))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'success': True, 'message': 'API backend Solu Africa Academy opérationnel.'})

    def test_course_catalog_and_detail_endpoints(self):
        response = self.client.get(reverse('academy:api-courses-list'))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload['results']), 1)
        self.assertEqual(payload['results'][0]['slug'], self.course.slug)

        detail = self.client.get(reverse('academy:api-course-detail', args=[self.course.slug]))
        self.assertEqual(detail.status_code, 200)
        self.assertEqual(detail.json()['result']['modules'][0]['lessons'][0]['slug'], self.lesson.slug)

    def test_register_login_and_me_endpoints(self):
        register_response = self.client.post(
            reverse('academy:api-register'),
            data=json.dumps(
                {
                    'username': 'mireille',
                    'email': 'mireille@example.com',
                    'password': 'VeryStrongPass123!',
                    'first_name': 'Mireille',
                    'last_name': 'Ekani',
                    'country': 'Côte d\'Ivoire',
                    'job_title': 'Data analyst',
                }
            ),
            content_type='application/json',
        )
        self.assertEqual(register_response.status_code, 201)
        self.assertEqual(register_response.json()['user']['username'], 'mireille')

        logout_response = self.client.post(reverse('academy:api-logout'))
        self.assertEqual(logout_response.status_code, 200)

        login_response = self.client.post(
            reverse('academy:api-login'),
            data=json.dumps({'username': 'mireille', 'password': 'VeryStrongPass123!'}),
            content_type='application/json',
        )
        self.assertEqual(login_response.status_code, 200)

        me_response = self.client.get(reverse('academy:api-me'))
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.json()['user']['email'], 'mireille@example.com')

    def test_enrollment_and_progress_endpoints(self):
        self.client.login(username='amina', password=self.password)

        enroll_response = self.client.post(
            reverse('academy:api-enrollments-create'),
            data=json.dumps({'course_slug': self.course.slug}),
            content_type='application/json',
        )
        self.assertEqual(enroll_response.status_code, 201)
        self.assertEqual(Enrollment.objects.count(), 1)
        self.assertEqual(LessonProgress.objects.count(), 1)

        progress_response = self.client.post(reverse('academy:api-progress-complete-lesson', args=[self.lesson.id]))
        self.assertEqual(progress_response.status_code, 200)
        self.assertEqual(progress_response.json()['result']['progress_percent'], 100)

        overview_response = self.client.get(reverse('academy:api-progress-overview'))
        self.assertEqual(overview_response.status_code, 200)
        self.assertEqual(overview_response.json()['results'][0]['modules'][0]['lessons'][0]['completed'], True)
