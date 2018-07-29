from django.contrib import admin
from .models import RawMaterial
from .forms import RawMaterialForm

# Register your models here.


class RawMaterialAdmin(admin.ModelAdmin):
    form = RawMaterialForm
    list_display = ('subject', 'sender', 'status', 'date_send', 'updated')

    list_filter = ('status', 'date_send', 'updated')

    def save_model(self, request, obj, form, change):
        obj.sender = request.user
        super().save_model(request, obj, form, change)


admin.site.register(RawMaterial, RawMaterialAdmin)
