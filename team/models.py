from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify


class Groups(models.Model):
    GROUP_CHOICES = [
        ('direcao', 'Direção'),
        ('secretaria', 'Secretaria'),
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
    

class Positions(models.Model):
    title = models.CharField(max_length=100, verbose_name='Cargo/Profissão')

    class Meta:
        verbose_name = 'Cargo/Profissão'
        verbose_name_plural = 'Cargo/Profissão'

    def __str__(self):
        return self.title


class Persons(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    image = models.ImageField(upload_to='team/%Y/%m', verbose_name='Foto', blank=True, null=True)
    positions = models.ManyToManyField(Positions, verbose_name='Cargo/Profissão', related_name='peoples')
    groups = models.ManyToManyField(Groups, verbose_name='Grupo a que pertence', related_name='people')
    slug = models.SlugField(unique=True, blank=True, max_length=120)
    about = HTMLField(blank=True, null=True, verbose_name='Excerto/Bibliografia')
    email = models.EmailField(max_length=200, blank=True, null=True, verbose_name='Email')

    class Meta:
        verbose_name = 'Corpo Docente e Não Docente'
        verbose_name_plural = 'Corpo Docente e Não Docente'

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name) or "pessoa"
            slug = base_slug
            counter = 1
            while Persons.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_positions_display(self):
        return ", ".join([str(pos) for pos in self.positions.all()])
    
    # verifica se existe alguma informação relevante,
    # caso não haja não mostra o botão saber mais no template, isto funciona junto com o if no template
    def has_portfolio(self):
        return (
            bool(self.about and self.about.strip()) or
            self.qualifications.exists() or
            self.experiences.exists() or
            self.fields.exists() or
            self.relevances.exists() or
            self.socials.exists()
        )

    def __str__(self):
        return self.name
    

class Qualification(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE, related_name='qualifications')
    qualification = models.CharField(max_length=100, blank=True, null=True, verbose_name='Formação Académica')

    class Meta:
        verbose_name = 'Formação Académica'
        verbose_name_plural = 'Formação Académica'

    def __str__(self):
        return self.qualification
    
    
class Experience(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE, related_name='experiences')
    experience = models.CharField(max_length=200, blank=True, null=True, verbose_name='Experiência Profissional')

    class Meta:
        verbose_name = 'Experiência Profissional'
        verbose_name_plural = 'Experiência Profissional'

    def __str__(self):
        return self.experience
    
    
class Field(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE, related_name='fields')
    field = models.CharField(max_length=200, blank=True, null=True, verbose_name='Área de Ensino')

    class Meta:
        verbose_name = 'Área de Ensino'
        verbose_name_plural = 'Áreas de Ensino'

    def __str__(self):
        return self.field
    
    
class Relevance(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE, related_name='relevances')
    relevance = models.CharField(max_length=200, blank=True, null=True, verbose_name='Destaques Profissionais')

    class Meta:
        verbose_name = 'Destaque Profissional'
        verbose_name_plural = 'Destaques Profissionais'

    def __str__(self):
        return self.relevance
    
    
class Social(models.Model):
    person = models.ForeignKey(Persons, on_delete=models.CASCADE, related_name='socials')
    social = models.URLField(max_length=500, blank=True, null=True, verbose_name='Link Rede Social')
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nome da Rede Social')

    class Meta:
        verbose_name = 'Rede Social'
        verbose_name_plural = 'Redes Sociais'

    def __str__(self):
        return self.social
