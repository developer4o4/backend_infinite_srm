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
    username = request.session.get('username')  
    admin_user = Admin_users.objects.filter(username=username).first()
    """Administrator uchun guruhlar ro'yxati"""
    groups = Groups.objects.filter(hwo_created=admin_user.username).order_by('-created_at')
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
from .models import Admin_users  
def admin_profil(request):
    # Foydalanuvchini sessiondan olish
    username = request.session.get('username')  # login paytida saqlangan bo‘lishi kerak
    if not username:
        messages.error(request, "Avval tizimga kiring.")
        return redirect('admin_login')  # kerakli login sahifaga yo‘naltirish

    admin_user = Admin_users.objects.filter(username=username).first()
    if not admin_user:
        messages.error(request, "Bunday foydalanuvchi topilmadi.")
        return redirect('admin_login')

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
        admin_user.phone_number = phone_number
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
                        messages.error(request, 'Yangi parol kamida 6 ta belgidan iborat bo‘lishi kerak.')
                else:
                    messages.error(request, 'Yangi parol va tasdiqlash paroli mos emas.')
            else:
                messages.error(request, 'Joriy parol noto‘g‘ri.')

        messages.success(request, 'Profil ma\'lumotlari yangilandi!')
        return redirect('admin_profil')

    # Session ma'lumotlarini yangilash
    request.session['first_name'] = admin_user.first_name
    request.session['last_name'] = admin_user.last_name

    context = {
        'admin_user': admin_user,
    }

    return render(request, 'administrator/admin_profile.html', context)

def create_group(request):
    if request.method == 'POST':
        try:
            # Form ma'lumotlarini olish
            title = request.POST.get('title')
            teacher_id = request.POST.get('teacher')
            group_price = request.POST.get('group_price')
            status = request.POST.get('status')
            group_time = request.POST.get('group_time')
            
            # Validatsiya
            if not all([title, teacher_id, group_price, status, group_time]):
                messages.error(request, "Barcha maydonlarni to'ldirishingiz kerak!")
                return render(request, 'groups/create_group.html', {
                    'teachers': Teachers.objects.all(),
                    'form_data': request.POST
                })
            
            # O'qituvchini topish
            teacher = get_object_or_404(Teachers, id=teacher_id)
            
            # Joriy admin foydalanuvchisi
            username = request.session.get('username')  # login paytida saqlangan bo‘lishi kerak
            if not username:
                messages.error(request, "Avval tizimga kiring.")
                return redirect('admin_login')  # kerakli login sahifaga yo‘naltirish

            current_admin = Admin_users.objects.filter(username=username).first()
            print(current_admin)
            # Yangi guruh yaratish
            group = Groups(
                title=title,
                teacher=teacher,
                group_price=group_price,
                status=status,
                group_time=group_time,
                hwo_created=current_admin
            )
            group.save()
            print(group)
            messages.success(request, f"'{title}' guruhi muvaffaqiyatli yaratildi!")
            return redirect('admin_gruppalar')
            
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return render(request, 'administrator/create_group.html', {
                'teachers': Teachers.objects.all(),
                'form_data': request.POST
            })
    
    else:
        # GET so'rovi - bo'sh formani ko'rsatish
        return render(request, 'administrator/create_group.html', {
            'teachers': Teachers.objects.all()
        })

def edit_group(request, group_id):
    group = get_object_or_404(Groups, id=group_id)
    
    if request.method == 'POST':
        try:
            # Form ma'lumotlarini olish
            title = request.POST.get('title')
            teacher_id = request.POST.get('teacher')
            group_price = request.POST.get('group_price')
            status = request.POST.get('status')
            group_time = request.POST.get('group_time')
            
            # Validatsiya
            if not all([title, teacher_id, group_price, status, group_time]):
                messages.error(request, "Barcha maydonlarni to'ldirishingiz kerak!")
                return render(request, 'groups/edit_group.html', {
                    'group': group,
                    'teachers': Teachers.objects.all()
                })
            
            # O'qituvchini topish
            teacher = get_object_or_404(Teachers, id=teacher_id)
            
            # Guruh ma'lumotlarini yangilash
            group.title = title
            group.teacher = teacher
            group.group_price = group_price
            group.status = status
            group.group_time = group_time
            group.save()
            
            messages.success(request, f"'{title}' guruhi muvaffaqiyatli yangilandi!")
            return redirect('groups_list')
            
        except Exception as e:
            messages.error(request, f"Xatolik yuz berdi: {str(e)}")
            return render(request, 'groups/edit_group.html', {
                'group': group,
                'teachers': Teachers.objects.all()
            })
    
    else:
        # GET so'rovi - mavjud ma'lumotlar bilan formani ko'rsatish
        return render(request, 'groups/edit_group.html', {
            'group': group,
            'teachers': Teachers.objects.all()
        })


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


def create_student(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        status = request.POST.get('status')
        about_student = request.POST.get('about_student', '')
        groups = request.POST.getlist('groups')  # For multiple group selection
        
        # Basic validation
        if not all([username, password, phone_number, first_name, last_name]):
            messages.error(request, "Iltimos, barcha kerakli maydonlarni to'ldiring.")
            return render(request, 'administrator/student_create.html', {
                'status_choices': Students.Status.choices,
                'groups': Groups.objects.all()  # Assuming Groups model is imported
            })
        
        # Check if username already exists
        if Students.objects.filter(username=username).exists():
            messages.error(request, "Bu foydalanuvchi nomi allaqachon mavjud.")
            return render(request, 'administrator/student_create.html', {
                'status_choices': Students.Status.choices,
                'groups': Groups.objects.all()
            })
        
        try:
            # Create new student
            student = Students(
                username=username,
                password=password,  # Will be hashed automatically in save method
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                status=status,
                about_student=about_student,
                admistrator=request.user.username  # Current administrator
            )
            
            # Save student
            student.save()
            
            # Add groups if any selected
            if groups:
                student.groups.set(groups)
            
            messages.success(request, "Student muvaffaqiyatli yaratildi!")
            return redirect('admin_oquvchilar')  # Redirect to students list page
            
        except Exception as e:
            messages.error(request, f"Student yaratishda xatolik: {str(e)}")
    
    # GET request - show empty form
    return render(request, 'administrator/student_create.html', {
        'status_choices': Students.Status.choices,
        'groups': Groups.objects.all()
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

def student_detail(request, student_uuid):
    try:
        student = Students.objects.get(uuid=student_uuid)
        student_groups = student.groups.all()
        all_groups = Groups.objects.all()
        
        context = {
            'student': student,
            'student_groups': student_groups,
            'groups_count': student_groups.count(),
            'all_groups': all_groups,
        }
        
        return render(request, 'administrator/student_detail.html', context)
        
    except Students.DoesNotExist:
        messages.error(request, "O'quvchi topilmadi")
        return redirect('admin_oquvchilar')

@require_POST
def student_edit(request, student_uuid):
    try:
        # AJAX so'rovni tekshirish
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        student = get_object_or_404(Students, uuid=student_uuid)
        
        # Asosiy ma'lumotlarni olish
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        phone_number = request.POST.get('phone_number', '').strip()
        status = request.POST.get('status', '').strip()
        role = request.POST.get('role', 'student').strip()
        about_student = request.POST.get('about_student', '').strip()
        
        # Validatsiya
        if not all([first_name, last_name, username, phone_number, status]):
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': 'Barcha kerakli maydonlarni to\'ldiring'
                })
            else:
                messages.error(request, "Barcha kerakli maydonlarni to'ldiring")
                return redirect('student_detail', student_uuid=student_uuid)
        
        # Username unikalligini tekshirish
        if Students.objects.filter(username=username).exclude(uuid=student_uuid).exists():
            if is_ajax:
                return JsonResponse({
                    'success': False,
                    'error': 'Bu username allaqachon mavjud'
                })
            else:
                messages.error(request, "Bu username allaqachon mavjud")
                return redirect('student_detail', student_uuid=student_uuid)
        
        # Ma'lumotlarni yangilash
        student.first_name = first_name
        student.last_name = last_name
        student.username = username
        student.phone_number = phone_number
        student.status = status
        student.role = role
        student.about_student = about_student
        
        # Guruhlarni yangilash
        selected_groups = request.POST.getlist('groups')
        student.groups.clear()  # Avvalgi guruhlarni tozalash
        
        for group_id in selected_groups:
            try:
                group = Groups.objects.get(id=group_id)
                student.groups.add(group)
            except Groups.DoesNotExist:
                continue
        
        student.save()
        
        if is_ajax:
            return JsonResponse({
                'success': True,
                'message': 'O\'quvchi ma\'lumotlari muvaffaqiyatli yangilandi'
            })
        else:
            messages.success(request, "O'quvchi ma'lumotlari muvaffaqiyatli yangilandi")
            return redirect('student_detail', student_uuid=student_uuid)
        
    except Exception as e:
        error_message = f'Xatolik yuz berdi: {str(e)}'
        if is_ajax:
            return JsonResponse({
                'success': False,
                'error': error_message
            })
        else:
            messages.error(request, error_message)
            return redirect('student_detail', student_uuid=student_uuid)