from django.urls import path
from . import views

app_name = 'festival'

urlpatterns = [
    path('festival/', views.festival, name='festival'),
]
