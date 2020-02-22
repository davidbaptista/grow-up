from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from grow_up import views

urlpatterns = [
    path('', include('administration.urls')),
    path('', include('authentication.urls')),
    path('', include('dashboard.urls')),
    path('', include('website.urls')),
    path('admin/', admin.site.urls),
    path('error/', views.error, name='error')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
