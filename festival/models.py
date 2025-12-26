from django.db import models
from tinymce.models import HTMLField # para editar os campos textfield e substituir por htmlfield


# model do festival
class Festival(models.Model):
    img = models.ImageField(upload_to='Festival/%Y/%m', verbose_name='Imagem do Festival', blank=True, null=True)
    description = HTMLField(verbose_name='Descrição do Evento')    
    address = models.CharField(max_length=100, verbose_name='Local de Realização')
    begin_date = models.DateField(verbose_name='Data de Início')
    end_date = models.DateField(verbose_name='Data de Encerramento')    
    link = models.URLField(max_length=500, verbose_name='Link de Informação', blank=True, null=True)
    link_name = models.CharField(max_length=100, verbose_name='Nome do Link', blank=True, null=True)

    class Meta:
        verbose_name = 'Festival'
        verbose_name_plural = 'Festival'

    def __str__(self):
        return self.address
