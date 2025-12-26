from django.contrib import admin
from .models import Group, Position, Person, ContactPenamacor


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('code', '__str__')

    def has_add_permission(self, request):
        return False  # ❌ Impede criação

    def has_delete_permission(self, request, obj=None):
        return False  # ❌ Impede exclusão

    def has_module_permission(self, request):
        return True  # ✅ Mostra no menu (ou False para esconder completamente)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_groups', 'get_positions')
    search_fields = ('name',)
    list_filter = ('groups', 'positions')  # Filtros laterais por grupo e cargo
    

    def get_groups(self, obj):
        return ", ".join([str(group) for group in obj.groups.all()])
    get_groups.short_description = 'Grupos'

    def get_positions(self, obj):
        return ", ".join([str(pos) for pos in obj.positions.all()])
    get_positions.short_description = 'Cargos'


@admin.register(ContactPenamacor)
class ContactPenamacorAdmin(admin.ModelAdmin):
    list_display = ('contact', 'email', 'time')