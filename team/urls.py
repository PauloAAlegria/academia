from django.urls import path
from . import views

app_name = 'team'

urlpatterns = [
    path('team/', views.team, name='team'),
    path('portfolio/<slug:slug>/', views.portfolio, name='portfolio'),
]
