from django.urls import path
from . import views

app_name = 'polo'

urlpatterns = [
    path('polo/', views.polo, name='polo'),
]
