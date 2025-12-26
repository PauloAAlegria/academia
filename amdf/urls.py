from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),  
    path('link/', views.link, name='link'),  
    path('gallery/', views.gallery, name='gallery'),
    path('course/<slug:slug>', views.course, name='course_detail'), # caminho para a página de detalhes de cada curso   
]
