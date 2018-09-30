from django.urls import path
from django.conf.urls import url
from django.contrib.auth.views import PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView

from . import views

urlpatterns = [
    path('', views.LoginView.as_view(), name='login'),
    path('password_reset/', PasswordResetView.as_view(template_name='reset_password.html'), name='password_reset'),
    path('password_reset/done', PasswordResetDoneView.as_view(template_name='reset_password_done.html'),
         name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('sign_up', views.sign_up_view, name='sign_up'),
    #url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #    views.activate, namespace='activate'),
    path('logout', views.logout_view, name='logout'),
    path('profile', views.client_profile, name='profile'),
    path('change_password', PasswordChangeView.as_view(template_name='change_password.html'), name='change_password'),
    path('update_personal_info', views.update_personal_info, name='update_personal_info'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('activate/<str:uid>/<str:token>', views.activate, name='activate')
]