from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from admistrators.models import Admin_users
from groups.models import Groups as Group
from students.models import Students as Student
from teachers.models import Teachers

def super_admin_dashboard(request):
    user = request.user
    context = {
        'user':user,
        'total_teachers': Teachers.objects.count(),
        'total_adminstrator': Admin_users.objects.count(),
        'total_students': Student.objects.count(),
        'total_groups': Group.objects.count(),
        'total_payments': 45200000,  # This would come from your payment model
    }
    return render(request, 'super_admin/dashboard.html', context)


def adminstratorlar(request):
    administrators = Admin_users.objects.all()
    context = {
        'administrators': administrators
    }
    return render(request, 'super_admin/adminstratorlar.html', context)

def gruppalar(request):
    groups = Group.objects.all()

    teachers = Teachers.objects.all()
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # Add new group
            name = request.POST.get('name')
            teacher_id = request.POST.get('teacher')
            course_price = request.POST.get('course_price')
            schedule = request.POST.get('schedule')
            status = request.POST.get('status')
            
            try:
                teacher = User.objects.get(id=teacher_id)
                group = Group.objects.create(
                    name=name,
                    teacher=teacher,
                    course_price=course_price,
                    schedule=schedule,
                    status=status
                )
                
                messages.success(request, 'Group successfully added!')
            except Exception as e:
                messages.error(request, f'Error adding group: {str(e)}')
        
        elif action == 'edit':
            # Edit existing group
            group_id = request.POST.get('group_id')
            name = request.POST.get('name')
            teacher_id = request.POST.get('teacher')
            course_price = request.POST.get('course_price')
            schedule = request.POST.get('schedule')
            status = request.POST.get('status')
            
            try:
                group = Group.objects.get(id=group_id)
                teacher = User.objects.get(id=teacher_id)
                
                group.name = name
                group.teacher = teacher
                group.course_price = course_price
                group.schedule = schedule
                group.status = status
                group.save()
                
                messages.success(request, 'Group successfully updated!')
            except Group.DoesNotExist:
                messages.error(request, 'Group not found!')
        
        elif action == 'delete':
            # Delete group
            group_id = request.POST.get('group_id')
            try:
                group = Group.objects.get(id=group_id)
                group.delete()
                
                messages.success(request, 'Group successfully deleted!')
            except Group.DoesNotExist:
                messages.error(request, 'Group not found!')
        
        return redirect('gruppalar')
    
    context = {
        'groups': groups,
        'teachers': teachers
    }
    
    return render(request, 'super_admin/gruppalar.html', context)

def oquvchilar(request):
    
    students = Student.objects.all()
    groups = Group.objects.filter(status='active')
    
    # Handle filters
    group_filter = request.GET.get('group_filter')
    status_filter = request.GET.get('status_filter')
    payment_filter = request.GET.get('payment_filter')
    
    if group_filter:
        students = students.filter(group_id=group_filter)
    if status_filter:
        students = students.filter(status=status_filter)
    if payment_filter:
        students = students.filter(payment_status=payment_filter)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add':
            # Add new student
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            group_id = request.POST.get('group')
            payment_status = request.POST.get('payment_status')
            status = request.POST.get('status')
            notes = request.POST.get('notes', '')
            
            try:
                group = Group.objects.get(id=group_id)
                student = Student.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone,
                    group=group,
                    payment_status=payment_status,
                    status=status,
                    notes=notes
                )
                
                messages.success(request, 'Student successfully added!')
            except Exception as e:
                messages.error(request, f'Error adding student: {str(e)}')
        
        elif action == 'edit':
            # Edit existing student
            student_id = request.POST.get('student_id')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            group_id = request.POST.get('group')
            payment_status = request.POST.get('payment_status')
            status = request.POST.get('status')
            notes = request.POST.get('notes', '')
            
            try:
                student = Student.objects.get(id=student_id)
                group = Group.objects.get(id=group_id)
                
                student.first_name = first_name
                student.last_name = last_name
                student.phone = phone
                student.group = group
                student.payment_status = payment_status
                student.status = status
                student.notes = notes
                student.save()
                
                messages.success(request, 'Student successfully updated!')
            except Student.DoesNotExist:
                messages.error(request, 'Student not found!')
        
        elif action == 'delete':
            # Delete student
            student_id = request.POST.get('student_id')
            try:
                student = Student.objects.get(id=student_id)
                student.delete()
                
                messages.success(request, 'Student successfully deleted!')
            except Student.DoesNotExist:
                messages.error(request, 'Student not found!')
        
        return redirect('oquvchilar')
    
    context = {
        'students': students,
        'groups': groups,
        'selected_group': group_filter,
        'selected_status': status_filter,
        'selected_payment': payment_filter
    }
    
    return render(request, 'super_admin/oquvchilar.html', context)

# API views for AJAX requests
def get_administrator_data(request, admin_id):
    try:
        administrator = Administrator.objects.get(id=admin_id)
        data = {
            'id': administrator.id,
            'first_name': administrator.user.first_name,
            'last_name': administrator.user.last_name,
            'username': administrator.user.username,
            'phone': administrator.phone,
            'status': 'active' if administrator.status else 'inactive'
        }
        return JsonResponse(data)
    except Administrator.DoesNotExist:
        return JsonResponse({'error': 'Administrator not found'}, status=404)

def get_group_data(request, group_id):
    """Get group data for editing"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        group = Group.objects.get(id=group_id)
        data = {
            'id': group.id,
            'name': group.name,
            'teacher_id': group.teacher.id,
            'course_price': group.course_price,
            'schedule': group.schedule,
            'status': group.status
        }
        return JsonResponse(data)
    except Group.DoesNotExist:
        return JsonResponse({'error': 'Group not found'}, status=404)

def get_student_data(request, student_id):
    try:
        student = Student.objects.get(id=student_id)
        data = {
            'id': student.id,
            'first_name': student.first_name,
            'last_name': student.last_name,
            'phone': student.phone,
            'group_id': student.group.id,
            'payment_status': student.payment_status,
            'status': student.status,
            'notes': student.notes
        }
        return JsonResponse(data)
    except Student.DoesNotExist:
        return JsonResponse({'error': 'Student not found'}, status=404)

def get_dashboard_stats(request):
    
    stats = {
        'total_users': User.objects.count(),
        'total_teachers': User.objects.filter(is_staff=True).count(),
        'total_students': Student.objects.count(),
        'total_groups': Group.objects.count(),
        'active_groups': Group.objects.filter(status='active').count(),
        'total_payments': 45200000,  # This would come from your payment model
    }
    
    return JsonResponse(stats)


def administrator_create(request):
    """Create new administrator"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Super admin privileges required.')
        return redirect('adminstratorlar')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        status = request.POST.get('status') == 'active'
        
        # Validate required fields
        if not all([first_name, last_name, username, phone, password]):
            messages.error(request, 'Iltimos, barcha maydonlarni to\'ldiring.')
            return redirect('administrator_create')
        
        # Check if username already exists
        if Admin_users.objects.filter(username=username).exists():
            messages.error(request, 'Bu login band. Boshqa login tanlang.')
            return redirect('administrator_create')
        
        try:
            # Create user
            user = Admin_users.objects.create(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                phone_number=phone
            )
            
            messages.success(request, f'Administrator {first_name} {last_name} muvaffaqiyatli qo\'shildi!')
            return redirect('adminstratorlar')
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
            # Clean up if user creation fails
            if Admin_users.objects.filter(username=username).exists():
                Admin_users.objects.filter(username=username).delete()
    
    return render(request, 'super_admin/adminstrator_create.html')

def administrator_detail(request, admin_id):
    
    administrator = get_object_or_404(Admin_users, id=admin_id)
    
    # Get groups managed by this administrator
    managed_groups = Group.objects.filter(hwo_created=administrator)
    
    context = {
        'admin': administrator,
        'managed_groups': managed_groups,
        'groups_count': managed_groups.count(),
        'active_groups': managed_groups.filter(status='active').count(),
        'inactive_groups': managed_groups.filter(status='inactive').count(),
    }
    
    return render(request, 'super_admin/adminstrator_detail.html', context)


def administrator_delete(request, admin_id):
    administrator = get_object_or_404(Admin_users, id=admin_id)
    admin_name = f"{administrator.first_name} {administrator.last_name}"
    
    try:
        # Check if administrator manages any groups
        managed_groups = Group.objects.filter(hwo_created=administrator)
        if managed_groups.exists():
            messages.error(request, f'{admin_name} guruhlarga biriktirilgan. Avval guruhlarni boshqa administratorga biriktiring.')
            return redirect('adminstratorlar')
        
        user = administrator
        administrator.delete()
        user.delete()
        
        messages.success(request, f'Administrator {admin_name} muvaffaqiyatli o\'chirildi!')
        
    except Exception as e:
        messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return redirect('adminstratorlar')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
import os
from django.conf import settings

# Role choices
ROLE_CHOICES = [
    ('administrator', 'Administrator'),
    ('moderator', 'Moderator'),
    ('teacher', "O'qituvchi"),
    ('assistant', 'Yordamchi'),
]

@login_required
def administrator_edit(request, admin_id):
    
    administrator = get_object_or_404(Admin_users, id=admin_id)
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        direction = request.POST.get('direction')
        role = request.POST.get('role')
        new_password = request.POST.get('password')
        profile_img = request.FILES.get('profile_img')
        
        # Validate required fields
        if not all([first_name, last_name, username, phone_number, direction, role]):
            messages.error(request, 'Iltimos, barcha majburiy maydonlarni to\'ldiring.')
            return render(request, 'administrators/edit.html', {
                'admin': administrator,
                'role_choices': ROLE_CHOICES,
                'current_role': administrator.role,
            })
        
        # Check if username already exists (excluding current admin)
        if Admin_users.objects.filter(username=username).exclude(id=admin_id).exists():
            messages.error(request, 'Bu login band. Boshqa login tanlang.')
            return render(request, 'administrators/edit.html', {
                'admin': administrator,
                'role_choices': ROLE_CHOICES,
                'current_role': administrator.role,
            })
        
        # Validate phone number
        if not phone_number.startswith('+998') or len(phone_number) != 13:
            messages.error(request, 'Iltimos, to\'g\'ri telefon raqamini kiriting (masalan: +998901234567).')
            return render(request, 'administrators/edit.html', {
                'admin': administrator,
                'role_choices': ROLE_CHOICES,
                'current_role': administrator.role,
            })
        
        # Validate password length if provided
        if new_password and len(new_password) < 6:
            messages.error(request, 'Parol kamida 6 ta belgidan iborat bo\'lishi kerak.')
            return render(request, 'administrators/edit.html', {
                'admin': administrator,
                'role_choices': ROLE_CHOICES,
                'current_role': administrator.role,
            })
        
        try:
            # Update administrator fields
            administrator.first_name = first_name
            administrator.last_name = last_name
            administrator.username = username
            administrator.phone_number = phone_number
            administrator.direction = direction
            administrator.role = role
            
            # Update profile image if provided
            if profile_img:
                # Delete old profile image if it's not default
                if administrator.profile_img and administrator.profile_img.name != 'profile.png':
                    old_image_path = os.path.join(settings.MEDIA_ROOT, administrator.profile_img.name)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                administrator.profile_img = profile_img
            
            # Update password if provided
            if new_password:
                administrator.set_password(new_password)
            
            administrator.save()
            
            messages.success(request, f'Administrator {first_name} {last_name} muvaffaqiyatli yangilandi!')
            return redirect('administrator_detail', admin_id=admin_id)
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
            return render(request, 'administrators/edit.html', {
                'admin': administrator,
                'role_choices': ROLE_CHOICES,
                'current_role': administrator.role,
            })
    
    context = {
        'admin': administrator,
        'role_choices': ROLE_CHOICES,
        'current_role': administrator.role,
    }
    
    return render(request, 'super_admin/adminstrator_edit.html', context)



# -------------------------------------- group -------------------   #
def group_detail(request, group_id):
    # Tanlangan guruhni olish
    group = get_object_or_404(Group, id=group_id)

    # Shu guruhga bog‘langan barcha studentlar
    students_in_group = Student.objects.filter(groups=group)

    # Statistika
    total_students = students_in_group.count()
    approved_students = students_in_group.filter(status=Student.Status.APPROVED).count()
    active_students = students_in_group.filter(status=Student.Status.GROUP).count()

    # Kontekst
    context = {
        'group': group,
        'students': students_in_group,
        'total_students': total_students,
        'approved_students': approved_students,
        'active_students': active_students,
        'teacher': group.teacher,
    }

    return render(request, 'super_admin/group_detail.html', context)

def group_edit(request, group_id):
    
    group = get_object_or_404(Group, id=group_id)
    teachers = Teachers.objects.all()
    
    if request.method == 'POST':
        title = request.POST.get('title')
        teacher_id = request.POST.get('teacher')
        group_price = request.POST.get('group_price')
        status = request.POST.get('status')
        group_time = request.POST.get('group_time')
        
        # Validate required fields
        if not all([title, teacher_id, group_price, status, group_time]):
            messages.error(request, 'Iltimos, barcha majburiy maydonlarni to\'ldiring.')
            return render(request, 'groups/edit.html', {
                'group': group,
                'teachers': teachers,
                'status_choices': Group.Status.choices,
            })
        
        try:
            teacher = Teachers.objects.get(id=teacher_id)
            group_price_int = int(group_price)
            
            if group_price_int < 0:
                messages.error(request, 'Guruh narxi manfiy bo\'lishi mumkin emas.')
                return render(request, 'groups/edit.html', {
                    'group': group,
                    'teachers': teachers,
                    'status_choices': Group.Status.choices,
                })
            
            # Update group
            group.title = title
            group.teacher = teacher
            group.group_price = group_price_int
            group.status = status
            group.group_time = group_time
            group.save()
            
            messages.success(request, f'Guruh "{title}" muvaffaqiyatli yangilandi!')
            return redirect('group_detail', group_id=group.id)
            
        except Teachers.DoesNotExist:
            messages.error(request, 'Tanlangan o\'qituvchi topilmadi.')
        except ValueError:
            messages.error(request, 'Guruh narxi to\'g\'ri formatda emas.')
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    context = {
        'group': group,
        'teachers': teachers,
        'status_choices': Group.Status.choices,
    }
    
    return render(request, 'super_admin/group_edit.html', context)


def group_delete(request, group_id):
    
    group = get_object_or_404(Group, id=group_id)
    group_name = group.title
    
    if request.method == 'POST':
        try:
            # Check if group has students
            if group.students.exists():
                messages.error(request, f'Guruhda {group.students.count()} ta o\'quvchi bor. Avval o\'quvchilarni boshqa guruhga o\'tkazing.')
                return redirect('group_detail', group_id=group_id)
            
            group.delete()
            messages.success(request, f'Guruh "{group_name}" muvaffaqiyatli o\'chirildi!')
            return redirect('gruppalar')
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
            return redirect('group_detail', group_id=group_id)
    
    # If not POST, show confirmation page
    context = {
        'group': group,
    }
    return render(request, 'super_admin/delete_group_confirm.html', context)

@login_required
def remove_student_from_group(request, group_id, student_uuid):
    """Remove student from group"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Super admin privileges required.')
        return redirect('group_detail', group_id=group_id)
    
    group = get_object_or_404(Group, id=group_id)
    student = get_object_or_404(Student, uuid=student_uuid)
    
    try:
        group.students.remove(student)
        messages.success(request, f'O\'quvchi {student.first_name} {student.last_name} guruhdan olib tashlandi!')
    except Exception as e:
        messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return redirect('group_detail', group_id=group_id)


# ----------------- student --------------- #
def student_detail(request, student_uuid):
    
    student = get_object_or_404(Student, uuid=student_uuid)
    
    # Get student's groups
    student_groups = student.groups.all()
    
    context = {
        'student': student,
        'student_groups': student_groups,
        'groups_count': student_groups.count(),
        'status_choices': Student.Status.choices,
    }
    
    return render(request, 'super_admin/student_detail.html', context)

@login_required
def student_edit(request, student_uuid):
    """Edit student view"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Super admin privileges required.')
        return redirect('oquvchilar')
    
    student = get_object_or_404(Student, uuid=student_uuid)
    groups = Group.objects.all()
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        status = request.POST.get('status')
        about_student = request.POST.get('about_student', '')
        selected_groups = request.POST.getlist('groups')
        new_password = request.POST.get('password')
        
        # Validate required fields
        if not all([first_name, last_name, username, phone_number, status]):
            messages.error(request, 'Iltimos, barcha majburiy maydonlarni to\'ldiring.')
            return render(request, 'students/edit.html', {
                'student': student,
                'groups': groups,
                'status_choices': Student.Status.choices,
            })
        
        # Check if username already exists (excluding current student)
        if Student.objects.filter(username=username).exclude(uuid=student_uuid).exists():
            messages.error(request, 'Bu login band. Boshqa login tanlang.')
            return render(request, 'students/edit.html', {
                'student': student,
                'groups': groups,
                'status_choices': Student.Status.choices,
            })
        
        # Validate phone number
        if not phone_number.startswith('+998') or len(phone_number) != 13:
            messages.error(request, 'Iltimos, to\'g\'ri telefon raqamini kiriting (masalan: +998901234567).')
            return render(request, 'students/edit.html', {
                'student': student,
                'groups': groups,
                'status_choices': Student.Status.choices,
            })
        
        # Validate password length if provided
        if new_password and len(new_password) < 6:
            messages.error(request, 'Parol kamida 6 ta belgidan iborat bo\'lishi kerak.')
            return render(request, 'students/edit.html', {
                'student': student,
                'groups': groups,
                'status_choices': Students.Status.choices,
            })
        
        try:
            # Update student
            student.first_name = first_name
            student.last_name = last_name
            student.username = username
            student.phone_number = phone_number
            student.status = status
            student.about_student = about_student
            student.admistrator = request.user.username
            
            # Update password if provided
            if new_password:
                student.set_password(new_password)
            
            student.save()
            
            # Update groups
            if selected_groups:
                student.groups.set(selected_groups)
            else:
                student.groups.clear()
            
            messages.success(request, f'O\'quvchi {first_name} {last_name} muvaffaqiyatli yangilandi!')
            return redirect('student_detail', student_uuid=student.uuid)
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    context = {
        'student': student,
        'groups': groups,
        'status_choices': Student.Status.choices,
        'student_groups': student.groups.all(),
    }
    
    return render(request, 'super_admin/student_edit.html', context)

@login_required
def student_delete(request, student_uuid):
    """Delete student view"""
    if not request.user.is_superuser:
        messages.error(request, 'Access denied. Super admin privileges required.')
        return redirect('oquvchilar')
    
    student = get_object_or_404(Student, uuid=student_uuid)
    student_name = f"{student.first_name} {student.last_name}"
    
    if request.method == 'POST':
        try:
            student.delete()
            messages.success(request, f'O\'quvchi {student_name} muvaffaqiyatli o\'chirildi!')
            return redirect('oquvchilar')
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
            return redirect('student_detail', student_uuid=student_uuid)
    
    # If not POST, show confirmation page
    context = {
        'student': student,
    }
    return render(request, 'super_admin/student_delete.html', context)

@login_required
def student_toggle_status(request, student_uuid):
    """Toggle student status via AJAX"""
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Access denied'})
    
    student = get_object_or_404(Students, uuid=student_uuid)
    
    try:
        # Cycle through statuses
        status_cycle = {
            'not_confirmed': 'approved',
            'approved': 'group', 
            'group': 'not_confirmed'
        }
        
        student.status = status_cycle.get(student.status, 'not_confirmed')
        student.save()
        
        status_display = dict(Students.Status.choices).get(student.status)
        
        return JsonResponse({
            'success': True,
            'new_status': student.status,
            'status_display': status_display
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})


def student_create(request):
    
    groups = Group.objects.all()
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        status = request.POST.get('status')
        about_student = request.POST.get('about_student', '')
        selected_groups = request.POST.getlist('groups')
        
        # Validate required fields
        if not all([first_name, last_name, username, phone_number, password, status]):
            messages.error(request, 'Iltimos, barcha majburiy maydonlarni to\'ldiring.')
            return render(request, 'students/create.html', {
                'groups': groups,
                'status_choices': Student.Status.choices,
                'form_data': request.POST
            })
        
        # Check if username already exists
        if Students.objects.filter(username=username).exists():
            messages.error(request, 'Bu login band. Boshqa login tanlang.')
            return render(request, 'students/create.html', {
                'groups': groups,
                'status_choices': Student.Status.choices,
                'form_data': request.POST
            })
        
        # Validate phone number
        if not phone_number.startswith('+998') or len(phone_number) != 13:
            messages.error(request, 'Iltimos, to\'g\'ri telefon raqamini kiriting (masalan: +998901234567).')
            return render(request, 'students/create.html', {
                'groups': groups,
                'status_choices': Student.Status.choices,
                'form_data': request.POST
            })
        
        # Validate password length
        if len(password) < 6:
            messages.error(request, 'Parol kamida 6 ta belgidan iborat bo\'lishi kerak.')
            return render(request, 'students/create.html', {
                'groups': groups,
                'status_choices': Student.Status.choices,
                'form_data': request.POST
            })
        
        try:
            # Create student
            student = Student(
                first_name=first_name,
                last_name=last_name,
                username=username,
                phone_number=phone_number,
                status=status,
                about_student=about_student,
                admistrator=request.user.username,
                password=password  # save method will hash it automatically
            )
            student.save()
            
            # Add groups if selected
            if selected_groups:
                student.groups.set(selected_groups)
            
            messages.success(request, f'O\'quvchi {first_name} {last_name} muvaffaqiyatli qo\'shildi!')
            return redirect('student_detail', student_uuid=student.uuid)
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
            return render(request, 'super_admin/student_create.html', {
                'groups': groups,
                'status_choices': Student.Status.choices,
                'form_data': request.POST
            })
    
    context = {
        'groups': groups,
        'status_choices': Student.Status.choices,
    }
    
    return render(request, 'super_admin/student_create.html', context)