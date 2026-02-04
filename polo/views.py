from django.shortcuts import render
from .models import Group, Person, ContactPenamacor

def polo(request):
    grupos = {
        "direcao": Group.objects.get(code="direcao"),
        "coordenacao": Group.objects.get(code="coordenacao"),
        "professores": Group.objects.get(code="professores"),
        "funcionarios": Group.objects.get(code="funcionarios"),
    }

    grupo_pessoas = {
        key: Person.objects.filter(groups=grupo).distinct()
        for key, grupo in grupos.items()
    }

    contato = ContactPenamacor.objects.first()

    return render(request, 'polo/polo.html', {
        "grupo_pessoas": grupo_pessoas, "contato": contato
    })