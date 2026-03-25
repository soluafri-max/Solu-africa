import json
from json import JSONDecodeError
from functools import wraps

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.db.models import Prefetch
from django.http import HttpRequest, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .models import Course, Enrollment, Lesson, LessonProgress, Module, StudentProfile

User = get_user_model()


LEVEL_LABELS = dict(Course.LEVEL_CHOICES)
STATUS_LABELS = dict(Enrollment.STATUS_CHOICES)


def parse_json(request: HttpRequest):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode('utf-8'))
    except (UnicodeDecodeError, JSONDecodeError):
        raise ValueError('Le corps de la requête doit être un JSON valide.')


def error_response(message: str, status: int = 400):
    return JsonResponse({'success': False, 'message': message}, status=status)


def api_login_required(view_func):
    @wraps(view_func)
    def wrapped(request: HttpRequest, *args, **kwargs):
        if not request.user.is_authenticated:
            return error_response('Authentification requise.', status=401)
        return view_func(request, *args, **kwargs)

    return wrapped


def lesson_to_dict(lesson: Lesson, completed: bool | None = None):
    payload = {
        'id': lesson.id,
        'title': lesson.title,
        'slug': lesson.slug,
        'content': lesson.content,
        'duration_minutes': lesson.duration_minutes,
        'video_url': lesson.video_url,
        'order': lesson.order,
        'is_preview': lesson.is_preview,
        'module_id': lesson.module_id,
    }
    if completed is not None:
        payload['completed'] = completed
    return payload


def module_to_dict(module: Module, include_lessons: bool = True):
    payload = {
        'id': module.id,
        'course_id': module.course_id,
        'title': module.title,
        'summary': module.summary,
        'order': module.order,
    }
    if include_lessons:
        payload['lessons'] = [lesson_to_dict(lesson) for lesson in module.lessons.all()]
    return payload


def course_to_dict(course: Course, include_modules: bool = False):
    payload = {
        'id': course.id,
        'title': course.title,
        'slug': course.slug,
        'short_description': course.short_description,
        'description': course.description,
        'level': course.level,
        'level_label': LEVEL_LABELS.get(course.level, course.level),
        'duration_weeks': course.duration_weeks,
        'is_published': course.is_published,
        'total_modules': course.modules.count(),
        'total_lessons': course.total_lessons,
        'created_at': course.created_at.isoformat(),
        'updated_at': course.updated_at.isoformat(),
    }
    if include_modules:
        payload['modules'] = [module_to_dict(module) for module in course.modules.all()]
    return payload


def profile_to_dict(profile: StudentProfile):
    return {
        'country': profile.country,
        'job_title': profile.job_title,
        'bio': profile.bio,
    }


def user_to_dict(user):
    profile, _ = StudentProfile.objects.get_or_create(user=user)
    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'profile': profile_to_dict(profile),
    }


def enrollment_to_dict(enrollment: Enrollment, include_progress: bool = False):
    payload = {
        'id': enrollment.id,
        'status': enrollment.status,
        'status_label': STATUS_LABELS.get(enrollment.status, enrollment.status),
        'enrolled_at': enrollment.enrolled_at.isoformat(),
        'progress_percent': enrollment.progress_percent,
        'completed_lessons': enrollment.completed_lessons,
        'course': course_to_dict(enrollment.course, include_modules=False),
    }
    if include_progress:
        completed_by_lesson = {
            progress.lesson_id: progress.completed
            for progress in enrollment.lesson_progress.select_related('lesson').all()
        }
        payload['modules'] = [
            {
                **module_to_dict(module, include_lessons=False),
                'lessons': [
                    lesson_to_dict(lesson, completed=completed_by_lesson.get(lesson.id, False))
                    for lesson in module.lessons.all()
                ],
            }
            for module in enrollment.course.modules.all()
        ]
    return payload


@require_GET
def health_check(_request: HttpRequest):
    return JsonResponse({'success': True, 'message': 'API backend Solu Africa Academy opérationnel.'})


@require_GET
def courses_list(_request: HttpRequest):
    queryset = Course.objects.filter(is_published=True).prefetch_related('modules__lessons')
    return JsonResponse({'success': True, 'results': [course_to_dict(course) for course in queryset]})


@require_GET
def course_detail(_request: HttpRequest, slug: str):
    course = get_object_or_404(
        Course.objects.filter(is_published=True).prefetch_related(
            Prefetch('modules', queryset=Module.objects.prefetch_related('lessons')),
        ),
        slug=slug,
    )
    return JsonResponse({'success': True, 'result': course_to_dict(course, include_modules=True)})


@require_GET
def module_detail(_request: HttpRequest, module_id: int):
    module = get_object_or_404(Module.objects.select_related('course').prefetch_related('lessons'), pk=module_id)
    return JsonResponse({'success': True, 'result': module_to_dict(module)})


@require_GET
def lesson_detail(_request: HttpRequest, lesson_id: int):
    lesson = get_object_or_404(Lesson.objects.select_related('module__course'), pk=lesson_id)
    return JsonResponse({'success': True, 'result': lesson_to_dict(lesson)})


@csrf_exempt
@require_POST
def register_user(request: HttpRequest):
    try:
        payload = parse_json(request)
    except ValueError as exc:
        return error_response(str(exc))

    username = (payload.get('username') or '').strip()
    email = (payload.get('email') or '').strip()
    password = payload.get('password') or ''
    first_name = (payload.get('first_name') or '').strip()
    last_name = (payload.get('last_name') or '').strip()

    if not username or not email or not password:
        return error_response('Les champs username, email et password sont obligatoires.')
    if User.objects.filter(username=username).exists():
        return error_response('Ce nom d’utilisateur existe déjà.', status=409)
    if User.objects.filter(email=email).exists():
        return error_response('Cet email est déjà utilisé.', status=409)

    user = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )
    StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'country': (payload.get('country') or '').strip(),
            'job_title': (payload.get('job_title') or '').strip(),
            'bio': (payload.get('bio') or '').strip(),
        },
    )
    login(request, user)
    return JsonResponse({'success': True, 'message': 'Compte créé avec succès.', 'user': user_to_dict(user)}, status=201)


@csrf_exempt
@require_POST
def login_user(request: HttpRequest):
    try:
        payload = parse_json(request)
    except ValueError as exc:
        return error_response(str(exc))

    username = (payload.get('username') or '').strip()
    password = payload.get('password') or ''
    if not username or not password:
        return error_response('Les champs username et password sont obligatoires.')

    user = authenticate(request, username=username, password=password)
    if user is None:
        return error_response('Identifiants invalides.', status=401)

    login(request, user)
    return JsonResponse({'success': True, 'message': 'Connexion réussie.', 'user': user_to_dict(user)})


@csrf_exempt
@require_POST
def logout_user(request: HttpRequest):
    logout(request)
    return JsonResponse({'success': True, 'message': 'Déconnexion réussie.'})


@api_login_required
@require_GET
def me(request: HttpRequest):
    return JsonResponse({'success': True, 'user': user_to_dict(request.user)})


@api_login_required
@require_GET
def enrollments_list(request: HttpRequest):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course').prefetch_related(
        'course__modules__lessons',
        'lesson_progress',
    )
    return JsonResponse({'success': True, 'results': [enrollment_to_dict(item) for item in enrollments]})


@csrf_exempt
@api_login_required
@require_POST
def create_enrollment(request: HttpRequest):
    try:
        payload = parse_json(request)
    except ValueError as exc:
        return error_response(str(exc))

    course_slug = (payload.get('course_slug') or '').strip()
    if not course_slug:
        return error_response('Le champ course_slug est obligatoire.')

    course = get_object_or_404(Course, slug=course_slug, is_published=True)
    enrollment, created = Enrollment.objects.get_or_create(user=request.user, course=course)
    for lesson in Lesson.objects.filter(module__course=course):
        LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)

    status = 201 if created else 200
    message = 'Inscription créée.' if created else 'Vous êtes déjà inscrit à cette formation.'
    enrollment = Enrollment.objects.select_related('course').get(pk=enrollment.pk)
    return JsonResponse({'success': True, 'message': message, 'result': enrollment_to_dict(enrollment, include_progress=True)}, status=status)


@api_login_required
@require_GET
def progress_overview(request: HttpRequest):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course').prefetch_related(
        Prefetch('course__modules', queryset=Module.objects.prefetch_related('lessons')),
        'lesson_progress',
    )
    return JsonResponse({'success': True, 'results': [enrollment_to_dict(item, include_progress=True) for item in enrollments]})


@csrf_exempt
@api_login_required
@require_POST
def complete_lesson(request: HttpRequest, lesson_id: int):
    lesson = get_object_or_404(Lesson.objects.select_related('module__course'), pk=lesson_id)
    enrollment = Enrollment.objects.filter(user=request.user, course=lesson.module.course).first()
    if enrollment is None:
        return error_response('Vous devez être inscrit à ce cours avant de marquer une leçon comme terminée.', status=403)

    progress, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
    progress.mark_completed()
    enrollment = Enrollment.objects.select_related('course').get(pk=enrollment.pk)
    return JsonResponse({'success': True, 'message': 'Leçon marquée comme terminée.', 'result': enrollment_to_dict(enrollment, include_progress=True)})
