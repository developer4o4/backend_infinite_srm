
from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.students, name="students"),
    path("students/add/", views.add_student, name="add_student"),
    path("students/edit/<uuid:uuid>/", views.edit_student, name="edit_student"),
    path("students/delete/<uuid:uuid>/", views.delete_student, name="delete_student"),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
]
