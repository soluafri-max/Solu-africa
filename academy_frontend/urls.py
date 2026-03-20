from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('programme/<slug:slug>/', views.program_detail, name='program_detail'),
    path('programme/<slug:slug>/lesson/', views.lesson_player, name='lesson_player'),
    path('communaute/', views.community, name='community'),
    path('admin-overview/', views.admin_overview, name='admin_overview'),
]
