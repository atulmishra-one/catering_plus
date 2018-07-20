from django.contrib import admin
from .models import User, Department
from django.contrib.auth.models import Group


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date_joined', 'is_active', 'departments', )
    fields = (('first_name', 'last_name'), ('email', 'password'),
              ('groups', 'user_permissions'), ('is_superuser', 'photo'), ('is_active', 'is_staff'))

    @classmethod
    def full_name(cls, obj):
        return "{0} {1}".format(obj.first_name, obj.last_name)

    @classmethod
    def departments(cls, obj):
        return "-".join([g.name for g in obj.groups.all()])


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Department)
