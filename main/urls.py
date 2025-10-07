from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.unified_login, name='unified_login'),
    path('logout/', views.custom_logout, name='logout'),
]