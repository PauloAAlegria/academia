from django.contrib import admin
from .models import Event, EventDetails

class EventDetailsInline(admin.StackedInline):    
    model = EventDetails
    extra = 1  # ou 4, depende dos que quiser colocar por padrão

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):   
    list_display = ['get_event_name', 'get_event_date'] 
    inlines = [EventDetailsInline]    

    def get_event_name(self, obj):
            detalhe = obj.eventos.first()  # "eventos" é o related_name do ForeignKey
            return detalhe.name if detalhe else '-'
    get_event_name.short_description = 'Nome do Evento'

    # def get_event_date(self, obj):
    #     detalhe = obj.eventos.first()
    #     return detalhe.date if detalhe else '-'
    # get_event_date.short_description = 'Data e Hora'

    def get_event_date(self, obj):
        detalhe = obj.eventos.first()
        return detalhe.date if detalhe and detalhe.date else '-'