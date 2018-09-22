from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Category
from .models import Meal
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

import json

# Create your views here.


class MealsView(TemplateView):
    template_name = 'meals_list.html'

    def get_context_data(self, **kwargs):
        slug = kwargs.get('slug', '')
        meals_list = Meal.objects.all()
        paginator = Paginator(meals_list, 1)
        page = self.request.GET.get('page')
        meals = paginator.get_page(page)
        if slug:
            slug = slug.split('/')
            categories_ = Category.objects.filter(slug__in=slug).all()
            meals_list = Meal.objects.filter(category_id__in=categories_).all()
            paginator = Paginator(meals_list, 50)
            page = self.request.GET.get('page')
            meals = paginator.get_page(page)
        self.kwargs.update({'meals': meals})
        return self.kwargs


