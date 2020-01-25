from django.contrib.auth.views import LogoutView
from django.urls import path

from website import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
