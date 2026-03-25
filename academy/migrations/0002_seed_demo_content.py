from django.db import migrations



def seed_demo_content(apps, schema_editor):
    Course = apps.get_model('academy', 'Course')
    Module = apps.get_model('academy', 'Module')
    Lesson = apps.get_model('academy', 'Lesson')

    python_course, _ = Course.objects.get_or_create(
        slug='python-pour-debutants',
        defaults={
            'title': 'Python pour débutants',
            'short_description': 'Maîtrisez les bases de Python avec une approche pratique.',
            'description': 'Initiez-vous à Python, aux structures de données et à la logique de programmation.',
            'level': 'beginner',
            'duration_weeks': 6,
            'is_published': True,
        },
    )
    django_course, _ = Course.objects.get_or_create(
        slug='developpement-web-avec-django',
        defaults={
            'title': 'Développement web avec Django',
            'short_description': 'Créez des applications web complètes avec Django.',
            'description': 'Travaillez sur les templates, les modèles, les formulaires et le déploiement.',
            'level': 'intermediate',
            'duration_weeks': 8,
            'is_published': True,
        },
    )

    python_module, _ = Module.objects.get_or_create(
        course=python_course,
        order=1,
        defaults={
            'title': 'Les fondamentaux Python',
            'summary': 'Découverte du langage, des variables et des boucles.',
        },
    )
    django_module, _ = Module.objects.get_or_create(
        course=django_course,
        order=1,
        defaults={
            'title': 'Django MVC et routage',
            'summary': 'Comprendre la structure d’un projet Django et son routage.',
        },
    )

    Lesson.objects.get_or_create(
        module=python_module,
        order=1,
        defaults={
            'title': 'Variables et types',
            'slug': 'variables-et-types',
            'content': 'Découvrez les types de base, les variables et les opérations essentielles.',
            'duration_minutes': 20,
            'is_preview': True,
        },
    )
    Lesson.objects.get_or_create(
        module=python_module,
        order=2,
        defaults={
            'title': 'Conditions et boucles',
            'slug': 'conditions-et-boucles',
            'content': 'Apprenez à contrôler le flux de votre programme.',
            'duration_minutes': 25,
            'is_preview': False,
        },
    )
    Lesson.objects.get_or_create(
        module=django_module,
        order=1,
        defaults={
            'title': 'Créer un projet Django',
            'slug': 'creer-un-projet-django',
            'content': 'Montez la structure de base d’un projet Django et comprenez les fichiers clés.',
            'duration_minutes': 22,
            'is_preview': True,
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ('academy', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed_demo_content, migrations.RunPython.noop),
    ]
