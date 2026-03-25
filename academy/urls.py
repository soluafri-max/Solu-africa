from django.urls import path

from . import api, views

app_name = 'academy'

urlpatterns = [
    path('', views.home, name='home'),
    path('formations/', views.courses, name='courses'),
    path('connexion/', views.auth_page, name='auth'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/health/', api.health_check, name='api-health'),
    path('api/courses/', api.courses_list, name='api-courses-list'),
    path('api/courses/<slug:slug>/', api.course_detail, name='api-course-detail'),
    path('api/modules/<int:module_id>/', api.module_detail, name='api-module-detail'),
    path('api/lessons/<int:lesson_id>/', api.lesson_detail, name='api-lesson-detail'),
    path('api/auth/register/', api.register_user, name='api-register'),
    path('api/auth/login/', api.login_user, name='api-login'),
    path('api/auth/logout/', api.logout_user, name='api-logout'),
    path('api/me/', api.me, name='api-me'),
    path('api/enrollments/', api.enrollments_list, name='api-enrollments-list'),
    path('api/enrollments/create/', api.create_enrollment, name='api-enrollments-create'),
    path('api/progress/', api.progress_overview, name='api-progress-overview'),
    path('api/progress/lessons/<int:lesson_id>/complete/', api.complete_lesson, name='api-progress-complete-lesson'),
]
