from django.db import models
from django.utils.text import slugify
from tinymce.models import HTMLField # para editar os campos textfield e substituir por htmlfield
from django.core.exceptions import ValidationError
from common.utils import process_image_field


# model para mudar o logo em todas as navbar
class LogoNavbar(models.Model):
    logo = models.ImageField(upload_to='logo_navbar/%Y/%m', blank=True, null=True, verbose_name='Logo Página Inicial')

    # para aparecer o nome da classe no admin com o nome correto
    class Meta:
        verbose_name = 'Logo Barra de Navegação'
        verbose_name_plural = 'Logo Barra de Navegação'
    
    def __str__(self):
        return 'Configuração do Site'


# model para mudar imagem e texto da página principal
class CoverPage(models.Model):
    cover_image = models.ImageField(upload_to='cover/%Y/%m', blank=True, null=True, verbose_name='Imagem do Site')
    academia_name = models.CharField(max_length=100, blank=True, default="", verbose_name='Nome da Academia')
    short_text = models.CharField(max_length=100, blank=True, default="", verbose_name='Frase Alusiva')

    # para aparecer o nome da classe no admin com o nome correto
    class Meta:
        verbose_name = 'Página Inicial'
        verbose_name_plural = 'Página Inicial'

    def __str__(self):
        return self.academia_name
    
    #alteração redimensionar imagem    
    def save(self, *args, **kwargs):
        process_image_field(self.cover_image)
        super().save(*args, **kwargs)    


# model para mudar o sobre a academia
class About(models.Model):
    title_1 = models.CharField(max_length=100, verbose_name='Título Página Principal')
    short_description = HTMLField(verbose_name='Descrição curta sobre a Academia')
    image_1 = models.ImageField(upload_to='about/%Y/%m', blank=True, null=True, verbose_name='Primeira Imagem')
    title_2 = models.CharField(max_length=100, blank=True, default="", verbose_name='Título Página do Sobre')
    long_description = HTMLField(verbose_name='Descrição longa sobre a Academia')
    image_2 = models.ImageField(upload_to='about/%Y/%m', blank=True, null=True, verbose_name='Segunda Imagem')
    image_3 = models.ImageField(upload_to='about/%Y/%m', blank=True, null=True, verbose_name='Terceira Imagem')

    # para aparecer o nome da classe no admin com o nome correto
    class Meta:
        verbose_name = 'Sobre a Academia'
        verbose_name_plural = 'Sobre a Academia'

    def __str__(self):
            return self.title_1
    
    #alteração redimensionar imagem    
    def save(self, *args, **kwargs):
        for field_name in ['image_1', 'image_2', 'image_3']:
            process_image_field(getattr(self, field_name))
        super().save(*args, **kwargs)    


# model dos cursos  
class Course(models.Model):    
    course_name = models.CharField(max_length=100, verbose_name='Nome do Curso')
    short_description = models.CharField(max_length=100, blank=True, default="", verbose_name='Texto Alusivo aos Cursos')
    course_name_2 = models.CharField(max_length=100, verbose_name='Título para Detalhes')
    portaria = models.CharField(max_length=100, blank=True, default="", verbose_name='Portaria / Decreto-Lei')
    instruments = HTMLField(verbose_name='Composição do Curso')

    # o slug é uma identificação única de cada curso, como uma chave primária
    slug = models.SlugField(unique=True, blank=True, max_length=120)

    # para aparecer o nome da classe no admin com o nome correto
    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        return self.course_name

    # gera automaticamente o slug com slugify(), mas garante que ele seja único na base de dados
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.course_name) or "curso"
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    

# model do rodapé
class Footer(models.Model):
    logo_amdf = models.ImageField(upload_to='logos_rodapé/%Y/%m', blank=True, null=True, verbose_name='Logo AMDF')
    logo_sc = models.ImageField(upload_to='logos_rodapé/%Y/%m', blank=True, null=True, verbose_name='Logo Santa Casa')
    logo_ed = models.ImageField(upload_to='logos_rodapé/%Y/%m', blank=True, null=True, verbose_name='Logo Educação')
    link_facebook = models.URLField(max_length=500, blank=True, null=True, verbose_name='Link do Facebook')
    link_instagram = models.URLField(max_length=500, blank=True, null=True, verbose_name='Link do Instagram')
    address = HTMLField(blank=True, null=True, verbose_name='Morada')
    contact = models.CharField(max_length=100, blank=True, default="", help_text="Exemplo: '+351 000 000 000'", verbose_name='Telemóvel/Telefone')
    email = models.CharField(max_length=100, blank=True, default="", verbose_name='Email')
    time = models.CharField(max_length=100, blank=True, default="", help_text="Exemplo: 'Seg a Sex - 08h00 às 21h00'", verbose_name='Horário de Funcionamento')

    # para aparecer o nome da classe no admin com o nome correto
    class Meta:
        verbose_name = 'Rodapé'
        verbose_name_plural = 'Rodapé'

    def __str__(self):
        return self.address


# model para a galeria
class Gallery(models.Model):
    title = models.CharField(max_length=100, verbose_name='Nome da Galeria')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Galeria'
        verbose_name_plural = 'Galeria'

class Midia(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='midias')
    title = models.CharField(max_length=100, blank=True, default="", verbose_name='Nome da Imagem ou Vídeo')
    image = models.ImageField(upload_to='galeria/imagem/%Y/%m', blank=True, null=True, verbose_name='Imagem')
    video = models.FileField(upload_to='galeria/videos/%Y/%m', blank=True, null=True, verbose_name='Vídeo')

    def __str__(self):
        return self.title or "Imagem sem nome"

    def is_image(self):
        return self.image and not self.video

    def is_video(self):
        return self.video and not self.image
    
    def clean(self):
        if self.image and self.video:
            raise ValidationError("Apenas um dos campos (imagem ou vídeo) deve ser preenchido.")
        if not self.image and not self.video:
            raise ValidationError("Um dos campos (imagem ou vídeo) deve ser preenchido.")

    #alteração redimensionar imagem    
    def save(self, *args, **kwargs):
        process_image_field(self.image)
        super().save(*args, **kwargs)    


# model para os downloads
class Download(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome do Ficheiro')
    link = models.URLField(max_length=500, verbose_name='Link do Ficheiro')

    class Meta:
        verbose_name = 'Downloads'
        verbose_name_plural = 'Downloads'

    def __str__(self):
        return self.name
    

# model para os links
class Link(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome do Ficheiro')
    link = models.URLField(max_length=500, verbose_name='Link do Ficheiro')

    class Meta:
        verbose_name = 'Critério de Avaliação'
        verbose_name_plural = 'Critérios de Avaliação'

    def __str__(self):
        return self.name
    

# Extra
# model para link do dev
class DevLink(models.Model):
    dev = models.URLField(max_length=500, blank=True, null=True, verbose_name='Link do Dev')

    class Meta:
        verbose_name = 'Link do Dev'
        verbose_name_plural = 'Link do Dev'

    def __str__(self):
        return self.dev