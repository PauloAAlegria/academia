from django.shortcuts import render, get_object_or_404
from .models import Groups, Persons


def team(request):
    grupos = {
        "direcao": Groups.objects.get(code="direcao"),
        "secretaria": Groups.objects.get(code="secretaria"),
        "professores": Groups.objects.get(code="professores"),
        "funcionarios": Groups.objects.get(code="funcionarios"),
    }

    grupos_pessoas = {
        key: Persons.objects.filter(groups=grupo).distinct()
        for key, grupo in grupos.items()
    }    

    return render(request, 'team/team.html', {
        "grupos_pessoas": grupos_pessoas
    })


# portfolio view: detalhe com todos os subdados
def portfolio(request, slug):
    persons = get_object_or_404(Persons, slug=slug)

    return render(request, 'team/portfolio.html', {
        'persons': persons,
        'qualifications': persons.qualifications.all(),
        'experiences': persons.experiences.all(),
        'fields': persons.fields.all(),
        'relevances': persons.relevances.all(),
        'socials': persons.socials.all()
    })