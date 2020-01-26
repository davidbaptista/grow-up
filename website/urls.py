from django.contrib.auth.views import LogoutView, PasswordResetView
from django.urls import path

from website import views
from website.forms import PasswordResetForm

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('organisation/', views.organisation, name='organisation'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', views.change_password, name='change-password'),
    path('reset-password/', PasswordResetView.as_view(template_name='authentication/password_reset.html',
                                                      form_class=PasswordResetForm),
         name='reset-password'),
    path('register-organisation/', views.register_organisation, name='register-organisation'),
    path('register-volunteer/', views.register_volunteer, name='register-volunteer'),

]
