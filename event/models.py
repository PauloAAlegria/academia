from django.db import models

# model para os eventos, passamos só a imagem
class Event(models.Model):
    image = models.ImageField(upload_to='eventos/%Y/%m', verbose_name='Imagem do Evento')    

    class Meta:
        verbose_name = 'Eventos'
        verbose_name_plural = 'Eventos'

    def __str__(self):
        return f"Evento #{self.id}"
    

# model para os detalhes dos eventos
class EventDetails(models.Model):
    poster = models.ForeignKey(Event, related_name='eventos', on_delete=models.CASCADE) 
    name = models.CharField(max_length=200, blank=True, default="", verbose_name='Nome do Evento')   
    local = models.CharField(max_length=200, blank=True, default="", verbose_name='Local de Realização')
    date = models.CharField(max_length=100, blank=True, default="", verbose_name='Data e Hora', help_text='Ex: 00/00/0000 às 00h00')
    link = models.URLField(null=True, blank=True, verbose_name='Link')

    def __str__(self):
        return self.local
