from django.urls import path

from . import views

app_name = 'academy'

urlpatterns = [
    path('', views.home, name='home'),
    path('formations/', views.courses, name='courses'),
    path('connexion/', views.auth_page, name='auth'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
