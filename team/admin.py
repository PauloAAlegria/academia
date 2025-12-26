from django.contrib import admin
from .models import (
    Groups,
    Positions,
    Persons,
    Qualification,
    Experience,
    Field,
    Relevance,
    Social
)


@admin.register(Groups)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('code', '__str__')

    def has_add_permission(self, request):
        return False  # ❌ Impede criação

    def has_delete_permission(self, request, obj=None):
        return False  # ❌ Impede exclusão

    def has_module_permission(self, request):
        return True  # ✅ Mostra no menu (ou False para esconder completamente)


@admin.register(Positions)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


class QualificationInLine(admin.TabularInline):
    model = Qualification
    extra = 1 # para mostrar um campo a mais


class ExperienceInLine(admin.TabularInline):
    model = Experience
    extra = 1 # para mostrar um campo a mais


class FieldInLine(admin.TabularInline):
    model = Field
    extra = 1 # para mostrar um campo a mais


class RelevanceInLine(admin.TabularInline):
    model = Relevance
    extra = 1 # para mostrar um campo a mais


class SocialInLine(admin.TabularInline):
    model = Social
    extra = 1 # para mostrar um campo a mais


@admin.register(Persons)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_groups', 'get_positions')
    search_fields = ('name',)
    list_filter = ('groups', 'positions')  # Filtros laterais por grupo e cargo
    inlines = [
        QualificationInLine,
        ExperienceInLine,
        FieldInLine,
        RelevanceInLine,
        SocialInLine
    ]    

    def get_groups(self, obj):
        return ", ".join([str(group) for group in obj.groups.all()])
    get_groups.short_description = 'Grupos'

    def get_positions(self, obj):
        return ", ".join([str(pos) for pos in obj.positions.all()])
    get_positions.short_description = 'Cargos'
