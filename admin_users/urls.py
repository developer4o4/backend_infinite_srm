from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.super_admin_dashboard, name='super_admin_dashboard'),
    path('super-admin/adminstratorlar/', views.adminstratorlar, name='adminstratorlar'),
    path('super-admin/gruppalar/', views.gruppalar, name='gruppalar'),
    path('super-admin/oquvchilar/', views.oquvchilar, name='oquvchilar'),
    path('super-admin/adminstratorlar/create/', views.administrator_create, name='administrator_create'),
    path('super-admin/adminstratorlar/<int:admin_id>/', views.administrator_detail, name='administrator_detail'),
    path('super-admin/adminstratorlar/<int:admin_id>/edit/', views.administrator_edit, name='administrator_edit'),
    path('super-admin/adminstratorlar/<int:admin_id>/delete/', views.administrator_delete, name='administrator_delete'),

    path('super-admin/gruppalar/<int:group_id>/', views.group_detail, name='group_detail'),
    path('super-admin/gruppalar/<int:group_id>/edit/', views.group_edit, name='group_edit'),
    path('super-admin/gruppalar/<int:group_id>/delete/', views.group_delete, name='group_delete'),
    path('super-admin/gruppalar/<int:group_id>/remove-student/<uuid:student_uuid>/', views.remove_student_from_group, name='remove_student_from_group'),

    path('super-admin/oquvchilar/<uuid:student_uuid>/', views.student_detail, name='student_detail'),
    path('super-admin/oquvchilar/create/', views.student_create, name='student_create'),
    path('super-admin/oquvchilar/<uuid:student_uuid>/edit/', views.student_edit, name='student_edit'),
    path('super-admin/oquvchilar/<uuid:student_uuid>/delete/', views.student_delete, name='student_delete'),
    path('super-admin/oquvchilar/<uuid:student_uuid>/toggle-status/', views.student_toggle_status, name='student_toggle_status'),
]