# Solu Africa Academy

Starter **Python + Django** pour une plateforme de formation nommée **Solu Africa Academy**, avec frontend de démonstration et backend API JSON.

## Ce que contient ce dépôt

- Une base de projet Django prête à lancer.
- Une app `academy` avec pages publiques, dashboard et backend métier.
- Un frontend avec templates Django, CSS et JavaScript.
- Une API JSON pour l’authentification, les formations, les inscriptions et la progression.

## Structure

```text
.
├── academy/
│   ├── migrations/
│   ├── admin.py
│   ├── api.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── solu_africa/
├── static/
├── templates/
├── manage.py
└── requirements.txt
```

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Routes frontend disponibles

- `/` : accueil
- `/formations/` : catalogue des formations
- `/connexion/` : page de connexion
- `/dashboard/` : tableau de bord apprenant

## API backend disponible

### Santé API
- `GET /api/health/`

### Authentification
- `POST /api/auth/register/`
- `POST /api/auth/login/`
- `POST /api/auth/logout/`
- `GET /api/me/`

### Catalogue
- `GET /api/courses/`
- `GET /api/courses/<slug>/`
- `GET /api/modules/<id>/`
- `GET /api/lessons/<id>/`

### Inscriptions et progression
- `GET /api/enrollments/`
- `POST /api/enrollments/create/`
- `GET /api/progress/`
- `POST /api/progress/lessons/<id>/complete/`

## Exemples de requêtes JSON

### Créer un compte

```bash
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "amina",
    "email": "amina@example.com",
    "password": "StrongPass123!",
    "first_name": "Amina",
    "last_name": "Ndiaye",
    "country": "Sénégal",
    "job_title": "Développeuse web"
  }'
```

### Se connecter

```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "amina", "password": "StrongPass123!"}'
```

### S’inscrire à une formation

```bash
curl -X POST http://127.0.0.1:8000/api/enrollments/create/ \
  -H "Content-Type: application/json" \
  -d '{"course_slug": "python-pour-debutants"}'
```

### Marquer une leçon comme terminée

```bash
curl -X POST http://127.0.0.1:8000/api/progress/lessons/1/complete/
```

## Admin

Le backend inclut l’administration Django pour gérer :
- les profils étudiants,
- les cours,
- les modules,
- les leçons,
- les inscriptions,
- la progression.

Accès : `/admin/`

## Tests

```bash
python manage.py test
```
