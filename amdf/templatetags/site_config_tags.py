# este templatetag - site_config_tags.py foi criado para inserir o logo em todas as navbar ao mesmo tempo

from django import template
from amdf.models import LogoNavbar

register = template.Library()

@register.simple_tag
def get_site_logo():
    config = LogoNavbar.objects.first()
    if config and config.logo:
        return config.logo.url
    return ''
