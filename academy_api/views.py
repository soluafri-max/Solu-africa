from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Enrollment, Lesson, LessonProgress, Module, Program, Subscription, SubscriptionPlan
from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    EnrollmentSerializer,
    LessonProgressSerializer,
    LessonSerializer,
    ModuleSerializer,
    ProgramSerializer,
    RegisterSerializer,
    SubscriptionPlanSerializer,
    SubscriptionSerializer,
    UserSerializer,
)


class RegisterAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'user': UserSerializer(user).data, 'token': token.key}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', '').lower()
        password = request.data.get('password', '')
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'user': UserSerializer(user).data, 'token': token.key})


class MeAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ProgramViewSet(viewsets.ModelViewSet):
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        queryset = Program.objects.select_related('category').prefetch_related('modules__lessons')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(is_published=True)

    @action(detail=True, methods=['get'], url_path='modules')
    def modules(self, request, slug=None):
        program = self.get_object()
        serializer = ModuleSerializer(program.modules.all(), many=True)
        return Response(serializer.data)


class ModuleViewSet(viewsets.ModelViewSet):
    serializer_class = ModuleSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Module.objects.select_related('program').prefetch_related('lessons')
        program_slug = self.request.query_params.get('program')
        if program_slug:
            queryset = queryset.filter(program__slug=program_slug)
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True, program__is_published=True)
        return queryset

    @action(detail=True, methods=['get'], url_path='lessons')
    def lessons(self, request, pk=None):
        module = self.get_object()
        serializer = LessonSerializer(module.lessons.all(), many=True)
        return Response(serializer.data)


class LessonViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Lesson.objects.select_related('module', 'module__program')
        module_id = self.request.query_params.get('module')
        if module_id:
            queryset = queryset.filter(module_id=module_id)
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True, module__is_published=True, module__program__is_published=True)
        return queryset


class EnrollmentViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Enrollment.objects.select_related('user', 'program', 'program__category')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='my')
    def my_enrollments(self, request):
        serializer = self.get_serializer(self.get_queryset().filter(user=request.user), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='unlock-status')
    def unlock_status(self, request, pk=None):
        enrollment = self.get_object()
        return Response(
            {
                'enrollment_id': enrollment.id,
                'program_id': enrollment.program_id,
                'subscription_status': 'active',
                'unlock_interval_days': 15 if enrollment.program.accelerated_unlock_enabled else enrollment.program.unlock_interval_days,
                'modules': enrollment.module_unlock_status(),
            }
        )


class ProgramProgressAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, slug):
        enrollment = Enrollment.objects.filter(user=request.user, program__slug=slug).select_related('program').first()
        if not enrollment:
            return Response({'detail': 'Enrollment not found.'}, status=status.HTTP_404_NOT_FOUND)

        lessons = Lesson.objects.filter(module__program=enrollment.program)
        progress_entries = LessonProgress.objects.filter(enrollment=enrollment)
        completed_lessons = progress_entries.filter(is_completed=True).count()
        total_lessons = lessons.count() or 1
        return Response(
            {
                'program': enrollment.program.title,
                'completed_lessons': completed_lessons,
                'total_lessons': total_lessons,
                'completion_percent': round((completed_lessons / total_lessons) * 100, 2),
            }
        )


class LessonWatchProgressAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        lesson = get_object_or_404(Lesson.objects.select_related('module__program'), pk=pk)
        enrollment = Enrollment.objects.filter(user=request.user, program=lesson.module.program).first()
        if not enrollment:
            return Response({'detail': 'Enrollment not found.'}, status=status.HTTP_404_NOT_FOUND)

        progress, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        serializer = LessonProgressSerializer(progress, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LessonCompleteAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        lesson = get_object_or_404(Lesson.objects.select_related('module__program'), pk=pk)
        enrollment = Enrollment.objects.filter(user=request.user, program=lesson.module.program).first()
        if not enrollment:
            return Response({'detail': 'Enrollment not found.'}, status=status.HTTP_404_NOT_FOUND)

        progress, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        progress.is_completed = True
        progress.completion_percent = 100
        progress.last_position_seconds = lesson.duration_seconds
        progress.watched_seconds = lesson.duration_seconds
        progress.save()
        return Response(LessonProgressSerializer(progress).data)


class SubscriptionPlanViewSet(viewsets.ModelViewSet):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(is_active=True)


class SubscriptionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Subscription.objects.select_related('plan', 'user')
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        subscription = self.get_queryset().filter(user=request.user).first()
        if not subscription:
            return Response({'detail': 'Subscription not found.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(subscription).data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def healthcheck(request):
    return Response({'status': 'ok', 'service': 'solu-africa-backend'})
