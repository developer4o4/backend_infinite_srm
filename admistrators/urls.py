from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/oquvchilar/', views.admin_oquvchilar, name='admin_oquvchilar'),
    path('admin/gruppalar/', views.admin_gruppalar, name='admin_gruppalar'),
    path('admin/profil/', views.admin_profil, name='admin_profil'),
    path('admin/gruppalar/<int:group_id>/', views.admin_group_detail, name='admin_group_detail'),
    path('admin/oquvchilar/<uuid:student_uuid>/', views.student_detail, name='admin_student_detail'),

    path('admin/group_create/',views.create_group,name="create_group"),
    path('admin/student_create/',views.create_student,name="student_create"),

    path('students/<uuid:student_uuid>/edit/', views.student_edit, name='student_edit'),
]