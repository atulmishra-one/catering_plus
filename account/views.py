from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import AuthenticationForm
from .forms import UserCreateForm, UserPersonalInfoChangeForm, ProfileForm
from django.contrib.auth.models import Group
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        email = form.data['username']
        password = form.data['password']

        user = authenticate(request, email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/profile')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def sign_up_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(request, email=email, password=raw_password)
            if user is not None:
                group = Group.objects.get(name='Clients')
                group.user_set.add(user.id)
                login(request, user)
                return redirect('/profile')
    else:
        form = UserCreateForm()
    return render(request, 'sign_up.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


@login_required
def client_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    return render(request, 'client_profile.html', {'profile': profile})


@login_required
def update_personal_info(request):
    if request.method == 'POST':
        form = UserPersonalInfoChangeForm(request.POST, instance=request.user)
    else:
        form = UserPersonalInfoChangeForm(instance=request.user)

    return render(request, 'update_personal_info.html', {'form': form})


@login_required
def update_profile(request):
    instance, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
        return redirect('/profile')
    else:
        form = ProfileForm(instance=instance)
    return render(request, 'update_profile.html', {'form': form})
