from django import template
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
register = template.Library()
from meal.models import Category
from django_currentuser.middleware import get_current_authenticated_user


@register.inclusion_tag(name='menus', filename='menus.html')
def menus():
    categories = Category.objects.all()
    return {
        'categories': categories,
        'get_current_user': get_current_authenticated_user
    }


@register.filter
def get_slugs(value):
    spam = value[:]
    spam = '/'.join(spam[-1:])
    return spam


@register.inclusion_tag(name='breadcrumb', filename='breadcrumb.html')
def breadcrumb(parent=None):
    bread_crumb = Category.objects.filter(parent=parent).all()
    return {
        'breadcrumb': bread_crumb
    }