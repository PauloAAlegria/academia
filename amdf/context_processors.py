from .models import Footer
from .models import DevLink


def footer_context(request):
    footer = Footer.objects.first()  # Pega o primeiro registro
    return {'footer': footer}


def dev_link(request):
    return {'dev_link': DevLink.objects.first()}
