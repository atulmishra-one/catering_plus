from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.views import AuthenticationForm
from .forms import UserCreateForm, UserPersonalInfoChangeForm, ProfileForm
from django.contrib.auth.models import Group
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from account.models import CaterUser

# Create your views here.


class LoginView(FormView):
    template_name = 'login.html'
    form_class = AuthenticationForm
    success_url = '/meals'

    def form_valid(self, form):
        email = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)
        if user is not None and user.is_active:
            login(self.request, user)
        return super().form_valid(form)


def sign_up_view(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Clients')
            group.user_set.add(user.id)
            current_site = get_current_site(request)
            mail_subject = 'Activate your Catering & Banquet account.'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)

            activation_link = "{0}/activate/{1}/{2}".format(current_site, force_text(uid), token)

            message = render_to_string('acc_active_email.html', {
                'user': user,
                'activation_link': activation_link
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.add_message(request, messages.SUCCESS,
                                 'Please confirm your email address to complete the registration.')
            return redirect('/sign_up')

            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(request, email=email, password=raw_password)
            #
            # if user is not None:
            #     group = Group.objects.get(name='Clients')
            #     group.user_set.add(user.id)
            #     login(request, user)
            #     return redirect('/profile')
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
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Saved!')
            form.save()
        return redirect('/update_personal_info')
    else:
        form = UserPersonalInfoChangeForm(instance=request.user)

    return render(request, 'update_personal_info.html', {'form': form})


@login_required
def update_profile(request):
    instance, _ = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=instance)
        if form.is_valid():
            messages.add_message(request, messages.SUCCESS, 'Saved!')
            form.save()
        return redirect('/profile')
    else:
        form = ProfileForm(instance=instance)
    return render(request, 'update_profile.html', {'form': form})


def activate(request, uid, token):
    try:
        uid_ = force_text(urlsafe_base64_decode(uid))
        user = CaterUser.objects.get(pk=uid_)
    except(TypeError, ValueError, OverflowError, CaterUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('/meals')
    else:
        return HttpResponse('Activation link is invalid!')

