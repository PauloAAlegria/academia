from django.shortcuts import render
from .models import Event

def event(request):
    posters = Event.objects.all()
    return render(request, 'event/event.html', {'posters': posters})
