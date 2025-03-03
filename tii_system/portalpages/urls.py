"""Module providing a function printing python version."""
from django.urls import path
from . import views

app_name = 'portalpages'

urlpatterns = [
    path('representative/', views.representative, name='representative'),
    path('agentdistributor/', views.agentdistributor, name='agentdistributor'),
    path('franchise/', views.franchise, name='franchise'),
    path('tracking/', views.tracking, name='tracking'),
    path('help/', views.homepage_help, name='help'),
    path('', views.home, name='home')
]
