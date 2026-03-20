from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    EnrollmentViewSet,
    LessonCompleteAPIView,
    LessonViewSet,
    LessonWatchProgressAPIView,
    LoginAPIView,
    MeAPIView,
    ModuleViewSet,
    ProgramProgressAPIView,
    ProgramViewSet,
    RegisterAPIView,
    SubscriptionPlanViewSet,
    SubscriptionViewSet,
    healthcheck,
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')
router.register('programs', ProgramViewSet, basename='program')
router.register('modules', ModuleViewSet, basename='module')
router.register('lessons', LessonViewSet, basename='lesson')
router.register('enrollments', EnrollmentViewSet, basename='enrollment')
router.register('plans', SubscriptionPlanViewSet, basename='plan')
router.register('subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='auth-register'),
    path('auth/login/', LoginAPIView.as_view(), name='auth-login'),
    path('auth/me/', MeAPIView.as_view(), name='auth-me'),
    path('learning/programs/<slug:slug>/progress/', ProgramProgressAPIView.as_view(), name='program-progress'),
    path('learning/lessons/<int:pk>/watch-progress/', LessonWatchProgressAPIView.as_view(), name='lesson-watch-progress'),
    path('learning/lessons/<int:pk>/complete/', LessonCompleteAPIView.as_view(), name='lesson-complete'),
    path('system/health/', healthcheck, name='system-health'),
    path('', include(router.urls)),
]
