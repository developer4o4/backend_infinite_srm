from django.contrib import admin
from django.urls import path, include
from .views import home
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', include('main.urls')),
    path('', home),
    path('super-admin/', include('admin_users.urls')),
    path('administrator/', include('admistrators.urls')),
    path('teacher/', include('teachers.urls')),
    path('student/', include('students.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)