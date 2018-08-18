from django.contrib import admin
from .models import CaterUser, Department, Profile
from django.contrib.auth.models import Group
from .forms import UserCreateAdmin


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    form = UserCreateAdmin
    list_display = ('full_name', 'email', 'date_joined', 'is_active', 'departments', )

    fields = (('first_name', 'last_name'), ('email', 'password'), ('phone_number', ),
              ('groups', 'user_permissions'), ('is_superuser', 'photo'), ('is_active', 'is_staff'))

    list_filter = ('is_staff', 'is_active', 'date_joined', 'groups')
    search_fields = ('full_name', )

    ordering = ('email', )

    @classmethod
    def full_name(cls, obj):
        return "{0} {1}".format(obj.first_name, obj.last_name)

    @classmethod
    def departments(cls, obj):
        return "-".join([g.name for g in obj.groups.all()])

    def save_model(self, request, obj, form, change):
        obj.set_password(form.cleaned_data['password'])
        super().save_model(request, obj, form, change)


admin.site.register(CaterUser, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Department)
admin.site.register(Profile)

