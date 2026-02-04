from django.shortcuts import render, get_object_or_404
from .models import Course, About, CoverPage, Midia, Download, Link
from django.http import HttpResponse


# view para a página inicial e para buscar e mostrar todos os cursos existentes
def home(request):
    cover = CoverPage.objects.first()
    about_data = About.objects.first() # passar os dados do sobre para a página index
    courses = Course.objects.all() # passar os dados do curso para a página do index
    return render(request, 'amdf/index.html', {'courses': courses, 'about': about_data, 'cover': cover})


# view para mostrar a parte sobre a academia
def about(request):
    about_data = About.objects.first() # passar os dados do sobre para a página do about
    return render(request, 'amdf/about.html', {'about': about_data})


# view para os detalhes de cada curso
def course(request, slug):
    course = get_object_or_404(Course, slug=slug) # passar os dados curso para a página do course através de uma identificação única (slug)
    return render(request, 'amdf/course.html', {'course': course})


# view para obter todos os objetos da galeria
def gallery(request):
    midias = Midia.objects.all()
    return render(request, 'amdf/gallery.html', {'midias': midias})


# view para obter todos os objetos para downloads e critérios de avaliação
def link(request):
    downloads = Download.objects.all().order_by('name')
    links = Link.objects.all().order_by('name')
    return render(request, 'amdf/link.html', {'downloads': downloads, 'links':links})