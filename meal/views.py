from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Category
from .models import Meal

import json

# Create your views here.


class MealsView(TemplateView):
    template_name = 'meals_list.html'

    def get_context_data(self, **kwargs):
        slug = kwargs.get('slug', '')
        categories = Category.objects.all()
        meals = Meal.objects.all()[0:50]

        breadcrumb = Category.objects.filter(parent=None)

        if slug:
            slug = slug.split('/')
            categories_ = Category.objects.filter(slug__in=slug).all()
            meals = Meal.objects.filter(category_id__in=categories_).all()
            breadcrumb = Category.objects.get(slug__in=slug).get_ancestors()

        self.kwargs.update({'categories': categories, 'meals': meals, 'breadcrumb': breadcrumb})
        return self.kwargs


