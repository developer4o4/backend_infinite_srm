
from django.shortcuts import render, redirect, get_object_or_404
from .models import Students
import uuid

def add_student(request):
    if request.method == "POST":
        Students.objects.create(
            username=request.POST['username'],
            password=request.POST['password'],
            phone_number=request.POST['phone_number'],
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            status=request.POST['status'],
            admistrator=request.POST['admistrator'],
        )
        return redirect("students")
    return render(request, "student/add_student.html", {
        "status_choices": Students.Status.choices   # 🔑 status yuboriladi
    })

def edit_student(request, uuid):
    student = get_object_or_404(Students, uuid=uuid)
    if request.method == "POST":
        student.username = request.POST['username']
        student.password = request.POST['password']
        student.phone_number = request.POST['phone_number']
        student.first_name = request.POST['first_name']
        student.last_name = request.POST['last_name']
        student.status = request.POST['status']
        student.admistrator = request.POST['admistrator']
        student.save()
        return redirect("students")
    return render(request, "student/edit_student.html", {
        "student": student,
        "status_choices": Students.Status.choices   # 🔑 status yuboriladi
    })

def delete_student(request, uuid):
    student = get_object_or_404(Students, uuid=uuid)
    if request.method == "POST":
        student.delete()
        return redirect("students")
    return render(request, "student/delete_student.html", {"student": student})


def students(request):
    all_students = Students.objects.all()
    context = {
        "students":all_students
    }
    return render(request,'student/students.html',context=context)


from django.shortcuts import render, redirect
from django.contrib import messages

def student_dashboard(request):
    if request.session.get('user_type') != 'student':
        messages.error(request, 'Sizga ushbu sahifaga kirish ruxsati yo\'q')
        return redirect('unified_login')
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'first_name': request.session.get('first_name'),
            'last_name': request.session.get('last_name'),
        }
    }
    return render(request, 'students/dashboard.html', context)