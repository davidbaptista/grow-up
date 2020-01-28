from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.urls import path

from website import views
from website.forms import PasswordResetForm, SetPasswordForm

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('organisation/', views.organisation, name='organisation'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-change/', views.password_change, name='password_change'),
    path('password-reset/',
         PasswordResetView.as_view(
             template_name='authentication/password_reset.html',
             form_class=PasswordResetForm,
             subject_template_name='authentication/password_reset_subject.txt',
             email_template_name='authentication/password_reset_email.html'),
         name='password_reset'),
    path('password-reset-done',
         PasswordResetDoneView.as_view(
             template_name='authentication/password_reset_done.html',
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name='authentication/password_reset_confirm.html',
             form_class=SetPasswordForm),
         name='password_reset_confirm'),
    path('password-reset-complete',
         PasswordResetCompleteView.as_view(
             template_name='authentication/password_reset_complete.html'),
         name='password_reset_complete'),
    path('register-organisation/', views.register_organisation, name='register_organisation'),
    path('register-volunteer/', views.register_volunteer, name='register_volunteer'),

]
