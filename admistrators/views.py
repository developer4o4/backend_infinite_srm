from django.shortcuts import render, redirect
from django.contrib import messages

def admin_dashboard(request):
    if request.session.get('user_type') != 'admin':
        messages.error(request, 'Sizga ushbu sahifaga kirish ruxsati yo\'q')
        return redirect('unified_login')
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'first_name': request.session.get('first_name'),
            'last_name': request.session.get('last_name'),
        }
    }
    return render(request, 'administrator/dashboard.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from students.models import Students
from groups.models import Groups
from teachers.models import Teachers

def admin_oquvchilar(request):
    """Administrator uchun o'quvchilar ro'yxati"""
    students = Students.objects.all().order_by('-created_ad')
    groups = Groups.objects.all()
    
    # Search va filter funksiyalari
    search_query = request.GET.get('search', '')
    group_filter = request.GET.get('group', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        students = students.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(username__icontains=search_query)
        )
    
    if group_filter:
        students = students.filter(groups__id=group_filter)
    
    if status_filter:
        students = students.filter(status=status_filter)
    
    # Statistika
    total_students = students.count()
    approved_students = students.filter(status='approved').count()
    group_students = students.filter(status='group').count()
    
    context = {
        'students': students,
        'groups': groups,
        'search_query': search_query,
        'group_filter': group_filter,
        'status_filter': status_filter,
        'total_students': total_students,
        'approved_students': approved_students,
        'group_students': group_students,
    }
    
    return render(request, 'administrator/oquvchilar.html', context)

def admin_gruppalar(request):
    """Administrator uchun guruhlar ro'yxati"""
    groups = Groups.objects.all().order_by('-created_at')
    teachers = Teachers.objects.all()
    
    # Search va filter funksiyalari
    search_query = request.GET.get('search', '')
    teacher_filter = request.GET.get('teacher', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        groups = groups.filter(title__icontains=search_query)
    
    if teacher_filter:
        groups = groups.filter(teacher__id=teacher_filter)
    
    if status_filter:
        groups = groups.filter(status=status_filter)
    
    # Statistika
    total_groups = groups.count()
    active_groups = groups.filter(status='active').count()
    total_students_in_groups = sum(group.students.count() for group in groups)
    
    context = {
        'groups': groups,
        'teachers': teachers,
        'search_query': search_query,
        'teacher_filter': teacher_filter,
        'status_filter': status_filter,
        'total_groups': total_groups,
        'active_groups': active_groups,
        'total_students_in_groups': total_students_in_groups,
    }
    
    return render(request, 'administrator/gruppalar.html', context)

def admin_profil(request):
    """Administrator profili"""
    admin_user = request.user
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone_number = request.POST.get('phone_number')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        # Profil ma'lumotlarini yangilash
        admin_user.first_name = first_name
        admin_user.last_name = last_name
        
        # Telefon raqamini yangilash (agar alohida model bo'lsa)
        try:
            admin_profile = Admin_users.objects.get(username=admin_user.username)
            admin_profile.phone_number = phone_number
            admin_profile.save()
        except:
            pass
        
        admin_user.save()
        
        # Parolni yangilash
        if current_password and new_password and confirm_password:
            if admin_user.check_password(current_password):
                if new_password == confirm_password:
                    if len(new_password) >= 6:
                        admin_user.set_password(new_password)
                        admin_user.save()
                        messages.success(request, 'Parol muvaffaqiyatli yangilandi!')
                    else:
                        messages.error(request, 'Yangi parol kamida 6 ta belgidan iborat bo\'lishi kerak.')
                else:
                    messages.error(request, 'Yangi parol va tasdiqlash paroli mos kelmadi.')
            else:
                messages.error(request, 'Joriy parol noto\'g\'ri.')
        
        messages.success(request, 'Profil ma\'lumotlari yangilandi!')
        return redirect('admin_profil')
    
    # Session ma'lumotlarini yangilash
    request.session['first_name'] = admin_user.first_name
    request.session['last_name'] = admin_user.last_name
    
    context = {
        'admin_user': admin_user,
    }
    
    return render(request, 'administrator/admin_profile.html', context)

def admin_group_detail(request, group_id):
    """Administrator uchun guruh tafsilotlari"""
    group = get_object_or_404(Groups, id=group_id)
    students = group.students.all()
    
    context = {
        'group': group,
        'students': students,
        'teacher': group.teacher,
        'total_students': students.count(),
    }
    
    return render(request, 'administrator/group_detail.html', context)

def admin_student_detail(request, student_uuid):
    """Administrator uchun o'quvchi tafsilotlari"""
    student = get_object_or_404(Students, uuid=student_uuid)
    student_groups = student.groups.all()
    
    context = {
        'student': student,
        'student_groups': student_groups,
        'groups_count': student_groups.count(),
    }
    
    return render(request, 'administrator/student_detail.html', context)