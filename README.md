# Solu Africa Academy

Starter frontend en **Python + Django** pour une plateforme de formation nommée **Solu Africa Academy**.

## Ce que contient ce dépôt

- Une base de projet Django prête à lancer.
- Une app `academy` pour les pages publiques et apprenant.
- Un frontend avec templates Django, CSS et JavaScript.
- Quatre pages de départ :
  - Accueil
  - Formations
  - Connexion
  - Dashboard apprenant

## Structure

```text
.
├── academy/
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
python manage.py runserver
```

## Routes disponibles

- `/` : accueil
- `/formations/` : catalogue des formations
- `/connexion/` : page de connexion
- `/dashboard/` : tableau de bord apprenant

## Tests

```bash
python manage.py test
```
