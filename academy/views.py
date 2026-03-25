from django.shortcuts import render

from .models import Course


COURSE_FALLBACKS = [
    {
        'title': 'Python pour débutants',
        'description': 'Maîtrisez les bases de Python avec des projets concrets orientés métier.',
        'level': 'Débutant',
    },
    {
        'title': 'Développement web avec Django',
        'description': 'Créez des applications web modernes avec Django, PostgreSQL et Bootstrap.',
        'level': 'Intermédiaire',
    },
    {
        'title': 'Data analyse avec Pandas',
        'description': 'Nettoyez, analysez et visualisez des données pour prendre de meilleures décisions.',
        'level': 'Intermédiaire',
    },
]

FEATURES = [
    'Parcours structurés en modules',
    'Suivi des progrès apprenants',
    'Projets pratiques et portfolio',
    'Communauté et mentorat',
]


LEVEL_LABELS = dict(Course.LEVEL_CHOICES)


def get_course_cards(limit: int | None = None):
    queryset = Course.objects.filter(is_published=True)
    if queryset.exists():
        course_list = queryset[:limit] if limit else queryset
        cards = [
            {
                'title': course.title,
                'description': course.short_description,
                'level': LEVEL_LABELS.get(course.level, course.level),
                'slug': course.slug,
            }
            for course in course_list
        ]
        if cards:
            return cards
    return COURSE_FALLBACKS[:limit] if limit else COURSE_FALLBACKS



def home(request):
    context = {
        'features': FEATURES,
        'courses': get_course_cards(limit=2),
    }
    return render(request, 'academy/home.html', context)



def courses(request):
    return render(request, 'academy/courses.html', {'courses': get_course_cards()})



def auth_page(request):
    return render(request, 'academy/auth.html')



def dashboard(request):
    context = {
        'student_name': request.user.first_name or request.user.username if request.user.is_authenticated else 'Amina',
        'progress': 68,
        'next_session': 'Samedi 10:00 UTC',
        'active_courses': get_course_cards(limit=2),
    }
    return render(request, 'academy/dashboard.html', context)
