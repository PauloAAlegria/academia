from django.db import transaction
from .models import Groups

def create_default_groups(sender, **kwargs):
    default_codes = [code for code, _ in Groups.GROUP_CHOICES]
    with transaction.atomic():
        for code in default_codes:
            Groups.objects.get_or_create(code=code)