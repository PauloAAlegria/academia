from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.admin.sites import NotRegistered, AlreadyRegistered
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.html import format_html
from .models import (
    LogoNavbar,
    CoverPage,
    About,
    Course,
    Footer,
    Gallery,
    Midia,
    Download,
    Link,
    DevLink
)


# Permitir apenas ao Superuser criar/excluir users
class CustomUserAdmin(DefaultUserAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return True

# Desregistra com segurança
try:
    admin.site.unregister(User)
except NotRegistered:
    pass

# Registra novamente com a classe personalizada
try:
    admin.site.register(User, CustomUserAdmin)
except AlreadyRegistered:
    pass


# Logo Navbar
@admin.register(LogoNavbar)
class LogoNavbarAdmin(admin.ModelAdmin):
    list_display = ['logo_preview']
    list_display_links = ['logo_preview']

    def logo_preview(self, obj):
        return bool(obj.logo)
    logo_preview.boolean = True
    logo_preview.short_description = "Tem Logo?"


# Página Inicial
@admin.register(CoverPage)
class CoverPageAdmin(admin.ModelAdmin):
    list_display = ['academia_name', 'short_text', 'has_image']
    list_display_links = ['academia_name']

    def has_image(self, obj):
        return bool(obj.cover_image)
    has_image.boolean = True
    has_image.short_description = "Imagem de Capa?"


# Sobre a Academia
@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ['title_1', 'title_2', 'has_all_images', 'preview_image_1']
    list_display_links = ['title_1']

    def has_all_images(self, obj):
        return all([obj.image_1, obj.image_2, obj.image_3])
    has_all_images.boolean = True
    has_all_images.short_description = "Todas as Imagens?"

    # extra: para mostrar a imagem selecionada na página principal da administração
    def preview_image_1(self, obj):
        if obj.image_1:
            return format_html('<img src="{}" style="height: 50px;" />', obj.image_1.url)
        return "-"
    preview_image_1.short_description = "Imagem 1"


# Cursos
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'portaria']
    prepopulated_fields = {'slug': ('course_name',)} # para gerar automaticamente o slug no admin quando se cria um curso novo
    search_fields = ['course_name', 'course_name_2']
    list_filter = ['course_name']
    list_display_links = ['course_name']


# Rodapé
@admin.register(Footer)
class FooterAdmin(admin.ModelAdmin):
    list_display = ['contact', 'email', 'logo_amdf_check', 'logo_sc_check', 'logo_ed_check']
    list_display_links = ['contact', 'email', 'logo_amdf_check', 'logo_sc_check', 'logo_ed_check']

    def logo_amdf_check(self, obj):
        return bool(obj.logo_amdf)
    logo_amdf_check.boolean = True
    logo_amdf_check.short_description = "Logo AMDF?"

    def logo_sc_check(self, obj):
        return bool(obj.logo_sc)
    logo_sc_check.boolean = True
    logo_sc_check.short_description = "Logo Santa Casa?"

    def logo_ed_check(self, obj):
        return bool(obj.logo_ed)
    logo_ed_check.boolean = True
    logo_ed_check.short_description = "Logo Educação?"


# Galeria
class MidiaInline(admin.TabularInline):
    model = Midia
    extra = 1

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [MidiaInline]


# Downloads e Critérios de Avaliação
@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'link']


# Extra
# Link do Dev
@admin.register(DevLink)
class Dev(admin.ModelAdmin):
    list_display = ['dev']