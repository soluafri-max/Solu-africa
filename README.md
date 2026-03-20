# Solu-africa

## Backend + frontend Django générés

Ce dépôt contient maintenant :

- un prototype frontend Django pour les interfaces principales ;
- un backend MVP Django REST Framework pour les APIs clés de Solu Africa Academy.

### APIs backend disponibles

- `/api/v1/auth/register/`
- `/api/v1/auth/login/`
- `/api/v1/auth/me/`
- `/api/v1/categories/`
- `/api/v1/programs/`
- `/api/v1/modules/`
- `/api/v1/lessons/`
- `/api/v1/enrollments/`
- `/api/v1/plans/`
- `/api/v1/subscriptions/`
- `/api/v1/system/health/`

### Frontend pages disponibles

- `/`
- `/catalogue/`
- `/dashboard/`
- `/programme/<slug>/`
- `/programme/<slug>/lesson/`
- `/communaute/`
- `/admin-overview/`

### Lancer le projet

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Structure

- `config/` : configuration Django
- `academy_frontend/` : vues, routes, templates et styles
- `academy_api/` : modèles, serializers, vues et routes API
- `docs/backend-api-spec.md` : spécification backend
- `openapi/solu-africa-academy.openapi.yaml` : contrat OpenAPI
