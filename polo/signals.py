from django.db import transaction
from .models import Group

# signals criado para definir os grupos do polo de penamacor automaticamente
def create_default_groups(sender, **kwargs):
    default_codes = [code for code, _ in Group.GROUP_CHOICES]
    with transaction.atomic():
        for code in default_codes:
            Group.objects.get_or_create(code=code)
            