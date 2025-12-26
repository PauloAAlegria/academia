from django.shortcuts import render
from .models import Festival


# view com verificação dos objectos do model, caso não exista nada, apresenta uma mensagem definida no template
def festival(request):
    festivals = Festival.objects.first()

    has_festival_info = False
    if festivals:
        has_festival_info = any([            
            festivals.description,
            festivals.img,
            festivals.address,
            festivals.begin_date,
            festivals.end_date,            
            festivals.link,
            festivals.link_name,
        ])

    return render(request, 'festival/festival.html', {
        'festivals': festivals,
        'has_festival_info': has_festival_info
    })