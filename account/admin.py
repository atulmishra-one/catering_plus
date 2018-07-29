from django.contrib import admin
from .models import User, Department, Profile
from django.contrib.auth.models import Group


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'date_joined', 'is_active', 'departments', )
    fields = (('first_name', 'last_name'), ('email', 'password'), ('phone_number', ),
              ('groups', 'user_permissions'), ('is_superuser', 'photo'), ('is_active', 'is_staff'))

    list_filter = ('is_staff', 'is_active', 'date_joined', 'groups')
    search_fields = ('full_name', )

    @classmethod
    def full_name(cls, obj):
        return "{0} {1}".format(obj.first_name, obj.last_name)

    @classmethod
    def departments(cls, obj):
        return "-".join([g.name for g in obj.groups.all()])


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Department)
admin.site.register(Profile)

