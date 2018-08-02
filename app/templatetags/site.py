from django import template
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
register = template.Library()


@register.simple_tag(name='site_title')
def site_title():
    return _(settings.SITE_TITLE)


@register.simple_tag(name='site_copyright')
def site_copyright():
    return {
        'text': _('Copyright &copy; '),
        'year': datetime.today().year
    }