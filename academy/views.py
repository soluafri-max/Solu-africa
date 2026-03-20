from django.shortcuts import render


COURSES = [
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


def home(request):
    context = {
        'features': FEATURES,
        'courses': COURSES[:2],
    }
    return render(request, 'academy/home.html', context)



def courses(request):
    return render(request, 'academy/courses.html', {'courses': COURSES})



def auth_page(request):
    return render(request, 'academy/auth.html')



def dashboard(request):
    context = {
        'student_name': 'Amina',
        'progress': 68,
        'next_session': 'Samedi 10:00 UTC',
        'active_courses': COURSES[:2],
    }
    return render(request, 'academy/dashboard.html', context)
