from django.urls import path

from website import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('organisation/', views.organisation, name='organisation'),
    path('volunteer/', views.volunteer, name='volunteer'),
]
