from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('administration.urls')),
    path('', include('authentication.urls')),
    path('', include('dashboard.urls')),
    path('', include('website.urls')),
    path('admin/', admin.site.urls),
]
