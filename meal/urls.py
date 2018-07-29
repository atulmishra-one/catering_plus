from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.MealsView.as_view(), name='meals_list'),
    url('(?P<slug>.+)', views.MealsView.as_view(), name='meals_list'),
]
