from django.contrib.auth.views import LogoutView
from django.urls import path

from website import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('organisation/', views.organisation, name='organisation'),
    path('volunteer/', views.volunteer, name='volunteer'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.login, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register-organisation/', views.register_organisation, name='register-organisation'),
    path('register-volunteer/', views.register_volunteer, name='register-volunteer'),

]
