# Backend MVP Django / DRF

Cette app expose un premier backend API pour Solu Africa Academy.

## Endpoints MVP inclus

- `POST /api/v1/auth/register/`
- `POST /api/v1/auth/login/`
- `GET /api/v1/auth/me/`
- `GET /api/v1/categories/`
- `GET /api/v1/programs/`
- `GET /api/v1/programs/{slug}/`
- `GET /api/v1/programs/{slug}/modules/`
- `GET /api/v1/modules/{id}/lessons/`
- `POST /api/v1/enrollments/`
- `GET /api/v1/enrollments/my/`
- `GET /api/v1/enrollments/{id}/unlock-status/`
- `GET /api/v1/learning/programs/{slug}/progress/`
- `POST /api/v1/learning/lessons/{id}/watch-progress/`
- `POST /api/v1/learning/lessons/{id}/complete/`
- `GET /api/v1/plans/`
- `POST /api/v1/subscriptions/`
- `GET /api/v1/subscriptions/me/`
- `GET /api/v1/system/health/`
