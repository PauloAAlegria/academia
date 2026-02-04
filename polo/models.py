from django.db import models
from tinymce.models import HTMLField
from common.utils import process_image_field


class Group(models.Model):
    GROUP_CHOICES = [
        ('direcao', 'Direção'),
        ('coordenacao', 'Coordenação'),
        ('professores', 'Professores'),
        ('funcionarios', 'Funcionários'),
    ]

    code = models.CharField(max_length=20, choices=GROUP_CHOICES, unique=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'

    def __str__(self):
        # Mostra o label legível no admin
        return dict(self.GROUP_CHOICES).get(self.code, self.code)
    

class Position(models.Model):
    title = models.CharField(max_length=100, verbose_name='Cargo/Profissão')

    class Meta:
        verbose_name = 'Cargo/Profissão'
        verbose_name_plural = 'Cargo/Profissão'

    def __str__(self):
        return self.title


class Person(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    image = models.ImageField(upload_to='polo/%Y/%m', verbose_name='Foto', blank=True, null=True)
    positions = models.ManyToManyField(Position, verbose_name='Cargo/Profissão', related_name='people') # Pessoa pode ter vários cargos
    groups = models.ManyToManyField(
        Group, verbose_name='Grupo a que pertence',        
        related_name='people') # Pessoa pode pertencer a vários grupos mas com escolhas limitadas

    class Meta:
        verbose_name = 'Corpo Docente e Não Docente'
        verbose_name_plural = 'Corpo Docente e Não Docente'

    def __str__(self):
        return self.name    

    #alteração redimensionar imagem    
    def save(self, *args, **kwargs):
        # Processa a imagem antes de salvar
        process_image_field(self.image)

        super().save(*args, **kwargs)    
    

class ContactPenamacor(models.Model):
    address = HTMLField(verbose_name='Morada')
    contact = models.CharField(max_length=100, verbose_name='Telefone/Telemóvel', help_text="Exemplo: '+351 000 000 000'")
    email = models.EmailField(max_length=150, verbose_name='Email', blank=True, default="")
    time = models.CharField(max_length=150, verbose_name='Horário de Funcionamento', help_text="Exemplo: 'Seg a Sex - 08h00 às 21h00'")

    class Meta:
        verbose_name = 'Contato'
        verbose_name_plural = 'Contato'

    def __str__(self):
        return self.address