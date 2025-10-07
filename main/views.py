from django.shortcuts import render, redirect
from django.contrib import messages
from admin_users.models import Admin_users
from admistrators.models import Admin_users as AdminModel
from teachers.models import Teachers
from students.models import Students

def unified_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type', 'super_admin')
        
        user = None
        redirect_url = None
        
        try:
            if user_type == 'super_admin':
                try:
                    user = Admin_users.objects.get(username=username)
                    if user.check_password(password) and user.role == 'admin':
                        redirect_url = 'super_admin_dashboard'
                    else:
                        messages.error(request, 'Login yoki parol noto\'g\'ri')
                except Admin_users.DoesNotExist:
                    messages.error(request, 'Super admin topilmadi')
            
            elif user_type == 'admin':
                try:
                    user = AdminModel.objects.get(username=username)
                    if user.check_password(password) and user.role == 'adminstrator':
                        redirect_url = 'admin_dashboard'
                    else:
                        messages.error(request, 'Login yoki parol noto\'g\'ri')
                except AdminModel.DoesNotExist:
                    messages.error(request, 'Administrator topilmadi')
            
            elif user_type == 'teacher':
                try:
                    user = Teachers.objects.get(username=username)
                    if user.check_password(password):
                        redirect_url = 'teacher_dashboard'
                    else:
                        messages.error(request, 'Login yoki parol noto\'g\'ri')
                except Teachers.DoesNotExist:
                    messages.error(request, 'O\'qituvchi topilmadi')
            
            elif user_type == 'student':
                try:
                    user = Students.objects.get(username=username)
                    if user.check_password(password):
                        redirect_url = 'student_dashboard'
                    else:
                        messages.error(request, 'Login yoki parol noto\'g\'ri')
                except Students.DoesNotExist:
                    messages.error(request, 'Talaba topilmadi')
            
            if user and redirect_url:
                # UUID ni string ga o'zgartirish
                user_id = getattr(user, 'id', None)
                if user_id is None:
                    user_id = str(getattr(user, 'uuid', None))
                
                request.session['user_id'] = user_id
                request.session['username'] = user.username
                request.session['user_type'] = user_type
                request.session['first_name'] = getattr(user, 'first_name', '')
                request.session['last_name'] = getattr(user, 'last_name', '')
                request.session['role'] = getattr(user, 'role', '')
                
                messages.success(request, f'Xush kelibsiz, {user.username}!')
                return redirect(redirect_url)
                
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    return render(request, 'login.html')
def custom_logout(request):
    request.session.flush()
    messages.success(request, 'Siz tizimdan chiqdingiz')
    return redirect('unified_login')