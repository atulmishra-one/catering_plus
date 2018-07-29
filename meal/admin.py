from django.contrib import admin

from mptt.admin import DraggableMPTTAdmin

from .models import Category, Meal

# Register your models here.


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_level_indent = 20
    mptt_indent_field = "name"
    list_display = ('tree_actions','indented_title',
                    'related_meals_count', 'related_meals_cumulative_count')
    list_display_links = ('indented_title',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
            qs,
            Meal,
            'category',
            'meals_cumulative_count',
            cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                                                Meal,
                                                'category',
                                                'meals_count',
                                                cumulative=False)
        return qs

    def related_meals_count(self, instance):
        return instance.meals_count
    related_meals_count.short_description = 'Related meals (for this specific category)'

    def related_meals_cumulative_count(self, instance):
        return instance.meals_cumulative_count
    related_meals_cumulative_count.short_description = 'Related meals (in tree)'


class MealAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'category', 'price')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Meal, MealAdmin)

