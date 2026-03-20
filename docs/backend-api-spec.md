# Solu Africa Academy — Spécification backend Django / Django REST Framework

## 1. Stack backend recommandée

- **Framework** : Django 5 + Django REST Framework
- **Authentification** : JWT (`djangorestframework-simplejwt`)
- **Base de données** : PostgreSQL
- **Cache / tâches différées** : Redis + Celery
- **Stockage médias** : AWS S3
- **Streaming vidéo** : CloudFront + URLs signées
- **Documentation API** : OpenAPI 3.1 + Swagger / ReDoc
- **Paiement** : Stripe ou Flutterwave selon le marché visé
- **Emails** : AWS SES, SendGrid ou Brevo

## 2. Architecture Django proposée

### Applications Django

- `accounts` : utilisateurs, rôles, profils, auth, permissions
- `catalog` : catégories, programmes, modules, leçons, ressources
- `learning` : progression, déblocage, historique de visionnage
- `quiz` : quiz, questions, réponses, résultats
- `billing` : abonnements, paiements, webhooks
- `certificates` : génération et vérification des certificats
- `community` : forums, posts, commentaires, likes, modération
- `notifications` : emails, notifications in-app
- `analytics` : statistiques d’usage et tableaux de bord admin
- `common` : utilitaires, mixins, constantes, audit logs

## 3. Principes d’API

- Préfixe commun : `/api/v1`
- Format des réponses : JSON
- Authentification : Bearer JWT
- Pagination : `page`, `page_size`
- Tri : `ordering`
- Recherche : `search`
- Filtrage : query params DRF filter backend
- Fuseau horaire : UTC côté serveur
- Dates : ISO 8601

## 4. Rôles

- **student** : suit les programmes, passe les quiz, interagit dans la communauté
- **instructor** : gère son contenu pédagogique si activé
- **admin** : gestion complète plateforme, contenus, paiements, modération
- **support** : consultation et support opérationnel limité

## 5. Règles métier essentielles

### Progression et déblocage des modules

- Le `module_1` est débloqué immédiatement à l’activation de l’inscription / abonnement.
- Le `module_n+1` est débloqué **30 jours** après la date de déblocage du module précédent.
- Si le mode accéléré est activé sur le programme ou globalement, l’intervalle devient **15 jours**.
- Un module peut aussi exiger :
  - le visionnage complet des leçons du module précédent ;
  - la réussite du quiz précédent avec score minimal.

### Abonnement

- Un utilisateur ne peut accéder aux contenus premium que si son abonnement est `active` ou en `grace_period`.
- Si l’abonnement expire, l’accès aux contenus premium est suspendu, mais la progression reste conservée.

### Certification

- Le certificat n’est généré que si :
  - tous les modules du programme sont terminés ;
  - tous les quiz obligatoires sont validés ;
  - le statut d’inscription est `completed`.

## 6. Modèle de réponse standard

### Succès

```json
{
  "success": true,
  "message": "Request completed successfully.",
  "data": {}
}
```

### Erreur

```json
{
  "success": false,
  "message": "Validation error.",
  "errors": {
    "email": ["This field is required."]
  }
}
```

## 7. Authentification et comptes

Base URL : `/api/v1/auth`

### 7.1 Inscription

**POST** `/register`

```json
{
  "first_name": "Awa",
  "last_name": "Diallo",
  "email": "awa@example.com",
  "phone": "+221770000000",
  "password": "StrongPassword123!",
  "password_confirm": "StrongPassword123!",
  "country": "SN",
  "accepted_terms": true
}
```

Réponse : création de compte + envoi email de vérification.

### 7.2 Vérification email

**POST** `/verify-email`

```json
{
  "token": "email_verification_token"
}
```

### 7.3 Connexion

**POST** `/login`

```json
{
  "email": "awa@example.com",
  "password": "StrongPassword123!"
}
```

Réponse : `access`, `refresh`, `user`.

### 7.4 Rafraîchir le token

**POST** `/token/refresh`

```json
{
  "refresh": "jwt_refresh_token"
}
```

### 7.5 Déconnexion

**POST** `/logout`

```json
{
  "refresh": "jwt_refresh_token"
}
```

### 7.6 Mot de passe oublié

**POST** `/forgot-password`

```json
{
  "email": "awa@example.com"
}
```

### 7.7 Réinitialiser le mot de passe

**POST** `/reset-password`

```json
{
  "token": "reset_token",
  "password": "NewStrongPassword123!",
  "password_confirm": "NewStrongPassword123!"
}
```

### 7.8 Profil connecté

**GET** `/me`

### 7.9 Mise à jour du profil

**PATCH** `/me`

```json
{
  "first_name": "Awa",
  "last_name": "Diallo",
  "phone": "+221770000111",
  "bio": "Entrepreneure et consultante.",
  "avatar": "https://cdn.example.com/avatar.jpg",
  "language": "fr"
}
```

### 7.10 Changer le mot de passe

**POST** `/change-password`

```json
{
  "current_password": "OldStrongPassword123!",
  "new_password": "NewStrongPassword123!",
  "new_password_confirm": "NewStrongPassword123!"
}
```

## 8. Gestion des utilisateurs et administration

Base URL : `/api/v1/users`

### 8.1 Lister les utilisateurs (admin)

**GET** `/`

Filtres : `role`, `status`, `search`, `is_email_verified`

### 8.2 Détail utilisateur (admin)

**GET** `/{id}`

### 8.3 Créer un utilisateur (admin)

**POST** `/`

### 8.4 Modifier un utilisateur (admin)

**PATCH** `/{id}`

### 8.5 Désactiver / réactiver un utilisateur

**POST** `/{id}/activate`

**POST** `/{id}/deactivate`

### 8.6 Affecter un rôle

**POST** `/{id}/assign-role`

```json
{
  "role": "instructor"
}
```

## 9. Catalogue, programmes, modules, leçons

Base URL : `/api/v1/catalog`

### 9.1 Catégories

- **GET** `/categories`
- **POST** `/categories` (admin)
- **GET** `/categories/{id}`
- **PATCH** `/categories/{id}` (admin)
- **DELETE** `/categories/{id}` (admin)

Exemple catégorie :

```json
{
  "name": "Entrepreneuriat",
  "slug": "entrepreneuriat",
  "description": "Créer et structurer son entreprise.",
  "is_active": true
}
```

### 9.2 Programmes / cours

- **GET** `/programs`
- **POST** `/programs` (admin/instructor)
- **GET** `/programs/{id}`
- **PATCH** `/programs/{id}` (admin/instructor)
- **DELETE** `/programs/{id}` (admin)
- **POST** `/programs/{id}/publish` (admin)
- **POST** `/programs/{id}/unpublish` (admin)

Filtres : `category`, `level`, `language`, `is_published`, `is_featured`

Exemple payload création :

```json
{
  "title": "Lancer son entreprise en Afrique",
  "slug": "lancer-son-entreprise-en-afrique",
  "short_description": "Programme structuré pour entrepreneurs.",
  "description": "Description complète du programme.",
  "category_id": 1,
  "level": "beginner",
  "language": "fr",
  "thumbnail": "https://cdn.example.com/program.jpg",
  "trailer_video_url": "https://cdn.example.com/trailer.m3u8",
  "subscription_required": true,
  "certificate_enabled": true,
  "accelerated_unlock_enabled": false,
  "unlock_interval_days": 30,
  "is_featured": true
}
```

### 9.3 Modules

- **GET** `/programs/{program_id}/modules`
- **POST** `/programs/{program_id}/modules` (admin/instructor)
- **GET** `/modules/{id}`
- **PATCH** `/modules/{id}` (admin/instructor)
- **DELETE** `/modules/{id}` (admin/instructor)
- **POST** `/modules/{id}/reorder` (admin/instructor)
- **POST** `/modules/{id}/publish` (admin/instructor)

Exemple payload module :

```json
{
  "title": "Module 1 - Fondations",
  "description": "Comprendre les bases de l’entrepreneuriat.",
  "position": 1,
  "unlock_delay_days": 0,
  "is_mandatory": true,
  "requires_previous_module_completion": false,
  "requires_quiz_pass": false,
  "minimum_quiz_score": null,
  "estimated_duration_minutes": 180
}
```

### 9.4 Leçons

- **GET** `/modules/{module_id}/lessons`
- **POST** `/modules/{module_id}/lessons` (admin/instructor)
- **GET** `/lessons/{id}`
- **PATCH** `/lessons/{id}` (admin/instructor)
- **DELETE** `/lessons/{id}` (admin/instructor)
- **POST** `/lessons/{id}/publish` (admin/instructor)
- **POST** `/lessons/{id}/video-signature` (auth)

Exemple payload leçon :

```json
{
  "title": "Identifier une opportunité rentable",
  "description": "Apprendre à évaluer un besoin marché.",
  "position": 1,
  "video_provider": "s3_cloudfront",
  "video_source_key": "programs/1/modules/1/lesson-1/master.m3u8",
  "duration_seconds": 1260,
  "is_preview": false,
  "is_downloadable": false,
  "transcript": "Texte de la vidéo",
  "attachments": [
    {
      "name": "Workbook.pdf",
      "file_url": "https://cdn.example.com/workbook.pdf"
    }
  ]
}
```

### 9.5 Ressources téléchargeables

- **GET** `/lessons/{lesson_id}/resources`
- **POST** `/lessons/{lesson_id}/resources` (admin/instructor)
- **DELETE** `/resources/{id}` (admin/instructor)

## 10. Inscriptions et accès aux programmes

Base URL : `/api/v1/enrollments`

### 10.1 S’inscrire à un programme

**POST** `/`

```json
{
  "program_id": 1
}
```

### 10.2 Mes inscriptions

**GET** `/my`

### 10.3 Détail d’une inscription

**GET** `/{id}`

### 10.4 État d’accès aux modules

**GET** `/{id}/unlock-status`

Réponse exemple :

```json
{
  "enrollment_id": 42,
  "program_id": 1,
  "subscription_status": "active",
  "unlock_interval_days": 30,
  "modules": [
    {
      "module_id": 1,
      "position": 1,
      "is_unlocked": true,
      "unlocked_at": "2026-03-01T00:00:00Z",
      "next_unlock_at": null
    },
    {
      "module_id": 2,
      "position": 2,
      "is_unlocked": false,
      "unlocked_at": null,
      "next_unlock_at": "2026-03-31T00:00:00Z"
    }
  ]
}
```

### 10.5 Recalculer le planning de déblocage (admin)

**POST** `/{id}/rebuild-unlock-schedule`

## 11. Progression pédagogique

Base URL : `/api/v1/learning`

### 11.1 Tableau de bord étudiant

**GET** `/dashboard`

Retourne : progression globale, programmes actifs, prochains modules, quiz en attente, certificats.

### 11.2 Progression d’un programme

**GET** `/programs/{program_id}/progress`

### 11.3 Marquer une leçon comme démarrée

**POST** `/lessons/{lesson_id}/start`

### 11.4 Mettre à jour le temps de visionnage

**POST** `/lessons/{lesson_id}/watch-progress`

```json
{
  "watched_seconds": 540,
  "last_position_seconds": 540,
  "completion_percent": 42.8,
  "is_completed": false
}
```

### 11.5 Terminer une leçon

**POST** `/lessons/{lesson_id}/complete`

### 11.6 Historique de visionnage

**GET** `/watch-history`

### 11.7 Progression par module

**GET** `/modules/{module_id}/progress`

### 11.8 Progression d’un étudiant par admin

**GET** `/students/{user_id}/progress` (admin/support)

## 12. Quiz et validation

Base URL : `/api/v1/quizzes`

### 12.1 Lister les quiz d’un module

**GET** `/modules/{module_id}`

### 12.2 Créer un quiz

**POST** `/modules/{module_id}` (admin/instructor)

```json
{
  "title": "Quiz Module 1",
  "description": "Validation des acquis du module 1",
  "passing_score": 70,
  "max_attempts": 3,
  "shuffle_questions": true,
  "is_mandatory": true,
  "time_limit_minutes": 20
}
```

### 12.3 Détail quiz

**GET** `/{quiz_id}`

### 12.4 Modifier quiz

**PATCH** `/{quiz_id}` (admin/instructor)

### 12.5 Ajouter une question

**POST** `/{quiz_id}/questions` (admin/instructor)

```json
{
  "text": "Qu’est-ce qu’un business model ?",
  "type": "single_choice",
  "explanation": "Le business model décrit comment l’entreprise crée de la valeur.",
  "points": 1,
  "options": [
    {"text": "Le logo de l’entreprise", "is_correct": false},
    {"text": "Le mode de création, livraison et capture de valeur", "is_correct": true}
  ]
}
```

### 12.6 Soumettre une tentative

**POST** `/{quiz_id}/submit`

```json
{
  "answers": [
    {
      "question_id": 10,
      "selected_option_ids": [22]
    }
  ]
}
```

Réponse : score, réussite, tentative restante.

### 12.7 Historique de résultats

- **GET** `/{quiz_id}/results/me`
- **GET** `/{quiz_id}/results` (admin/instructor)

## 13. Abonnements et paiements

Base URL : `/api/v1/billing`

### 13.1 Lister les plans tarifaires

**GET** `/plans`

### 13.2 Créer un plan tarifaire (admin)

**POST** `/plans`

```json
{
  "name": "Mensuel Academy",
  "code": "monthly_academy",
  "amount": 29.99,
  "currency": "USD",
  "interval": "month",
  "trial_days": 7,
  "is_active": true
}
```

### 13.3 Démarrer un abonnement

**POST** `/subscriptions/checkout-session`

```json
{
  "plan_id": 1,
  "provider": "stripe",
  "success_url": "https://www.soluafricaacademy.com/payment/success",
  "cancel_url": "https://www.soluafricaacademy.com/payment/cancel"
}
```

### 13.4 Confirmer un abonnement

**POST** `/subscriptions/confirm`

```json
{
  "provider": "stripe",
  "session_id": "cs_test_123"
}
```

### 13.5 Mon abonnement actuel

**GET** `/subscriptions/me`

### 13.6 Annuler renouvellement auto

**POST** `/subscriptions/me/cancel`

### 13.7 Réactiver abonnement

**POST** `/subscriptions/me/reactivate`

### 13.8 Historique paiements

**GET** `/payments/me`

### 13.9 Paiements admin

**GET** `/payments` (admin)

Filtres : `status`, `provider`, `date_from`, `date_to`, `user_id`

### 13.10 Webhooks paiement

- **POST** `/webhooks/stripe`
- **POST** `/webhooks/flutterwave`

## 14. Certificats

Base URL : `/api/v1/certificates`

### 14.1 Lister mes certificats

**GET** `/my`

### 14.2 Générer un certificat

**POST** `/generate`

```json
{
  "program_id": 1
}
```

### 14.3 Télécharger un certificat

**GET** `/{id}/download`

### 14.4 Vérifier un certificat publiquement

**GET** `/verify/{certificate_number}`

Réponse : nom étudiant, programme, date d’émission, statut.

## 15. Communauté

Base URL : `/api/v1/community`

### 15.1 Lister les espaces / forums

- **GET** `/forums`
- **POST** `/forums` (admin)

### 15.2 Lister les posts

**GET** `/posts`

Filtres : `forum_id`, `program_id`, `author_id`, `search`, `pinned`

### 15.3 Créer un post

**POST** `/posts`

```json
{
  "forum_id": 1,
  "title": "Comment structurer une étude de marché ?",
  "content": "Je voudrais vos retours sur les étapes à suivre.",
  "tags": ["etude-marche", "debutant"]
}
```

### 15.4 Détail d’un post

- **GET** `/posts/{id}`
- **PATCH** `/posts/{id}`
- **DELETE** `/posts/{id}`

### 15.5 Commentaires

- **GET** `/posts/{id}/comments`
- **POST** `/posts/{id}/comments`
- **PATCH** `/comments/{id}`
- **DELETE** `/comments/{id}`

### 15.6 Interactions

- **POST** `/posts/{id}/like`
- **DELETE** `/posts/{id}/like`
- **POST** `/comments/{id}/like`
- **DELETE** `/comments/{id}/like`

### 15.7 Modération

- **POST** `/posts/{id}/pin` (admin/moderator)
- **POST** `/posts/{id}/lock` (admin/moderator)
- **POST** `/posts/{id}/report`
- **GET** `/reports` (admin/moderator)

## 16. Notifications

Base URL : `/api/v1/notifications`

### 16.1 Mes notifications

**GET** `/`

### 16.2 Marquer comme lue

**POST** `/{id}/read`

### 16.3 Marquer tout comme lu

**POST** `/read-all`

### 16.4 Préférences de notification

- **GET** `/preferences`
- **PATCH** `/preferences`

## 17. Analytics et reporting

Base URL : `/api/v1/analytics`

### 17.1 Vue d’ensemble admin

**GET** `/overview`

KPIs : nouveaux inscrits, abonnements actifs, churn, MRR, taux de complétion, taux de réussite quiz.

### 17.2 Revenus

**GET** `/revenue`

### 17.3 Engagement étudiants

**GET** `/engagement`

### 17.4 Performance programme

**GET** `/programs/{program_id}`

### 17.5 Export CSV

**GET** `/exports/students.csv`

**GET** `/exports/payments.csv`

## 18. Endpoints d’administration plateforme

Base URL : `/api/v1/admin`

### 18.1 Tableau de bord admin

**GET** `/dashboard`

### 18.2 Paramètres globaux plateforme

- **GET** `/settings`
- **PATCH** `/settings`

Exemples de réglages :

```json
{
  "default_unlock_interval_days": 30,
  "accelerated_unlock_interval_days": 15,
  "accelerated_mode_enabled": false,
  "certificate_signatory_name": "Direction Solu Africa Academy",
  "maintenance_mode": false
}
```

### 18.3 Jobs et tâches asynchrones

- **GET** `/jobs`
- **POST** `/jobs/rebuild-certificates`
- **POST** `/jobs/recompute-analytics`

## 19. Système vidéo et sécurité contenu

### Endpoints vidéo

Base URL : `/api/v1/video`

- **POST** `/sign-url`
- **POST** `/webhook/encoding`
- **GET** `/lessons/{lesson_id}/playback`

### Règles de sécurité

- Les URLs de lecture doivent être signées et expirer rapidement.
- Les leçons premium exigent abonnement actif.
- Les événements de lecture doivent être journalisés pour calculer la progression.
- Le téléchargement direct des vidéos doit être désactivé sauf exception explicite.

## 20. Healthchecks et ops

Base URL : `/api/v1/system`

- **GET** `/health`
- **GET** `/readiness`
- **GET** `/liveness`
- **GET** `/version`

## 21. Permissions par domaine

### Étudiants

- lire catalogue publié
- s’inscrire aux programmes
- accéder aux modules débloqués
- soumettre quiz
- télécharger certificats acquis
- publier en communauté

### Instructeurs

- créer / modifier programmes, modules, leçons, quiz selon droits
- consulter statistiques de leurs contenus

### Admins

- accès total
- gestion utilisateurs, paiements, contenu, modération, paramètres

## 22. Ordre conseillé d’implémentation côté backend

### Sprint 1 — Fondation

- auth JWT
- utilisateurs / rôles
- catégories
- programmes
- modules
- leçons

### Sprint 2 — Apprentissage

- inscriptions
- progression
- suivi vidéo
- déblocage 30 jours / 15 jours

### Sprint 3 — Monétisation

- plans
- abonnements
- paiements
- webhooks

### Sprint 4 — Validation

- quiz
- scoring
- certificats PDF

### Sprint 5 — Engagement

- communauté
- notifications
- analytics

## 23. Arborescence REST finale récapitulative

```text
/api/v1/
  auth/
  users/
  catalog/
  enrollments/
  learning/
  quizzes/
  billing/
  certificates/
  community/
  notifications/
  analytics/
  admin/
  video/
  system/
```

## 24. Recommandations DRF d’implémentation

- Utiliser `ViewSet` + `Router` pour les CRUD standard.
- Utiliser `APIView` pour login, webhooks, téléchargement certificat, génération URL signée.
- Mettre en place `django-filter` pour le filtrage.
- Utiliser permissions DRF custom :
  - `IsAdminUser`
  - `IsInstructorOrAdmin`
  - `IsEnrolledAndSubscriptionActive`
  - `CanAccessUnlockedModule`
- Ajouter `select_related` / `prefetch_related` pour optimiser les listes.
- Journaliser les événements critiques : login, paiement, génération certificat, changement de rôle.
- Prévoir tests : unitaires, intégration API, permissions, webhooks.

## 25. Endpoints MVP minimum

Pour livrer rapidement le MVP, implémenter au minimum :

- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/catalog/programs`
- `GET /api/v1/catalog/programs/{id}`
- `GET /api/v1/catalog/programs/{program_id}/modules`
- `GET /api/v1/catalog/modules/{id}`
- `GET /api/v1/catalog/modules/{module_id}/lessons`
- `POST /api/v1/enrollments`
- `GET /api/v1/enrollments/my`
- `GET /api/v1/enrollments/{id}/unlock-status`
- `POST /api/v1/learning/lessons/{lesson_id}/watch-progress`
- `POST /api/v1/learning/lessons/{lesson_id}/complete`
- `GET /api/v1/learning/programs/{program_id}/progress`
- `GET /api/v1/billing/plans`
- `POST /api/v1/billing/subscriptions/checkout-session`
- `POST /api/v1/billing/webhooks/stripe`
```
