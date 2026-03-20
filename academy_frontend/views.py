from django.shortcuts import render

PROGRAMS = [
    {
        'slug': 'lancer-son-entreprise-en-afrique',
        'title': 'Lancer son entreprise en Afrique',
        'category': 'Entrepreneuriat',
        'level': 'Débutant',
        'duration': '12 semaines',
        'students': 1240,
        'progress': 36,
        'description': 'Construire une idée viable, créer son modèle économique et démarrer ses premières ventes.',
        'modules': [
            {'title': 'Module 1 — Fondations', 'status': 'Débloqué', 'unlock': 'Disponible maintenant'},
            {'title': 'Module 2 — Étude de marché', 'status': 'Planifié', 'unlock': 'Déblocage le 31 mars 2026'},
            {'title': 'Module 3 — Finance entrepreneuriale', 'status': 'Verrouillé', 'unlock': '30 jours après le module 2'},
            {'title': 'Module 4 — Croissance', 'status': 'Verrouillé', 'unlock': '30 jours après le module 3'},
        ],
        'highlights': [
            'Progression pédagogique structurée sur 30 jours par module',
            'Quiz de validation et certification finale',
            'Accès communauté et suivi de progression',
        ],
    },
    {
        'slug': 'maitriser-son-budget-et-sa-tresorerie',
        'title': 'Maîtriser son budget et sa trésorerie',
        'category': 'Éducation financière',
        'level': 'Intermédiaire',
        'duration': '8 semaines',
        'students': 860,
        'progress': 72,
        'description': 'Piloter sa trésorerie, sécuriser ses marges et mieux décider grâce aux indicateurs financiers.',
        'modules': [
            {'title': 'Module 1 — Budget personnel', 'status': 'Débloqué', 'unlock': 'Disponible maintenant'},
            {'title': 'Module 2 — Lecture des flux', 'status': 'Débloqué', 'unlock': 'Débloqué le 15 mars 2026'},
            {'title': 'Module 3 — Prévisions', 'status': 'Planifié', 'unlock': 'Déblocage le 14 avril 2026'},
        ],
        'highlights': [
            'Tableaux simples et cas pratiques',
            'Suivi de la progression leçon par leçon',
            'Téléchargement de ressources PDF',
        ],
    },
]

COMMUNITY_POSTS = [
    {
        'author': 'Awa Diallo',
        'role': 'Étudiante',
        'title': 'Comment tester mon idée avant de lancer ? ',
        'content': 'Je cherche un cadre simple pour valider mon marché avec peu de budget.',
        'replies': 18,
        'likes': 41,
        'tag': 'Validation marché',
    },
    {
        'author': 'Samuel K.',
        'role': 'Coach',
        'title': '3 erreurs à éviter sur la gestion de trésorerie',
        'content': 'Voici un retour d’expérience terrain pour les entrepreneurs en phase de lancement.',
        'replies': 12,
        'likes': 57,
        'tag': 'Finance',
    },
]

STATS = {
    'students': '4 280',
    'subscriptions': '1 920',
    'completion_rate': '68%',
    'monthly_revenue': '$54 300',
}


def base_context():
    featured = PROGRAMS[0]
    return {
        'programs': PROGRAMS,
        'featured_program': featured,
        'community_posts': COMMUNITY_POSTS,
        'stats': STATS,
    }


def home(request):
    context = {
        **base_context(),
        'page_title': 'Accueil',
    }
    return render(request, 'academy_frontend/home.html', context)


def catalogue(request):
    context = {
        **base_context(),
        'page_title': 'Catalogue',
    }
    return render(request, 'academy_frontend/catalogue.html', context)


def dashboard(request):
    current_program = PROGRAMS[0]
    context = {
        **base_context(),
        'page_title': 'Dashboard étudiant',
        'current_program': current_program,
        'tasks': [
            'Terminer la leçon 3 du module 1',
            'Passer le quiz du module 1 (score minimum 70%)',
            'Télécharger le workbook “Business Model Canvas”',
        ],
        'notifications': [
            'Votre prochain module sera débloqué le 31 mars 2026.',
            'Le live communauté sur la trésorerie démarre vendredi à 18h UTC.',
        ],
    }
    return render(request, 'academy_frontend/dashboard.html', context)


def program_detail(request, slug):
    program = next((item for item in PROGRAMS if item['slug'] == slug), PROGRAMS[0])
    context = {
        **base_context(),
        'page_title': program['title'],
        'program': program,
    }
    return render(request, 'academy_frontend/program_detail.html', context)


def lesson_player(request, slug):
    program = next((item for item in PROGRAMS if item['slug'] == slug), PROGRAMS[0])
    context = {
        **base_context(),
        'page_title': 'Lecture vidéo',
        'program': program,
        'lesson': {
            'title': 'Identifier une opportunité rentable',
            'duration': '21 min',
            'completion': 42,
            'description': 'Comprendre les signaux marché, les frustrations clients et les premiers tests à mener.',
        },
    }
    return render(request, 'academy_frontend/lesson_player.html', context)


def community(request):
    context = {
        **base_context(),
        'page_title': 'Communauté',
    }
    return render(request, 'academy_frontend/community.html', context)


def admin_overview(request):
    context = {
        **base_context(),
        'page_title': 'Admin overview',
        'admin_cards': [
            {'label': 'Nouveaux inscrits', 'value': '326', 'trend': '+12% vs mois dernier'},
            {'label': 'Churn abonnement', 'value': '4.8%', 'trend': '-0.6 pt'},
            {'label': 'Quiz réussis', 'value': '81%', 'trend': '+5 pt'},
            {'label': 'Certificats générés', 'value': '612', 'trend': '+18%'},
        ],
    }
    return render(request, 'academy_frontend/admin_overview.html', context)
