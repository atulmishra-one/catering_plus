from django.contrib.auth.forms import UserCreationForm
from account.models import User, Profile
from django import forms


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        exclude = ('user_permissions', 'groups', 'is_superuser', 'last_login', 'password', 'is_active', 'is_staff')

        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data["email"]
            if commit:
                user.save()
            return user


class UserPersonalInfoChangeForm(forms.ModelForm):
    class Meta:
        model = User
        exclude = ('user_permissions', 'groups', 'is_superuser', 'last_login',
                   'password', 'is_active', 'is_staff', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


