from django.contrib import admin
from django.urls import path, include
from website import views

urlpatterns = [
    path('', include('website.urls')),
    path('', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]
