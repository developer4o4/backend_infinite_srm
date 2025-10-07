from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Teachers
from django.contrib.auth.hashers import make_password, check_password

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = make_password(request.POST['password'])
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        direction = request.POST['direction']
        phone_number = request.POST['phone_number']

        if Teachers.objects.filter(username=username).exists():
            messages.error(request, 'Bunday foydalanuvchi allaqachon mavjud!')
            return redirect('signup')

        Teachers.objects.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            direction=direction,
            phone_number=phone_number
        )
        messages.success(request, 'Ro‘yxatdan o‘tish muvaffaqiyatli!')
        return redirect('login')

    return render(request, 'teacher/signup.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            teacher = Teachers.objects.get(username=username)
        except Teachers.DoesNotExist:
            messages.error(request, 'Foydalanuvchi topilmadi!')
            return redirect('login')

        if check_password(password, teacher.password):
            request.session['teacher_id'] = teacher.id
            messages.success(request, f'Xush kelibsiz, {teacher.first_name}!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Parol noto‘g‘ri!')
            return redirect('login')

    return render(request, 'teacher/login.html')


from django.shortcuts import render, redirect
from django.contrib import messages

def teacher_dashboard(request):
    if request.session.get('user_type') != 'teacher':
        messages.error(request, 'Sizga ushbu sahifaga kirish ruxsati yo\'q')
        return redirect('unified_login')
    
    context = {
        'user': {
            'username': request.session.get('username'),
            'first_name': request.session.get('first_name'),
            'last_name': request.session.get('last_name'),
        }
    }
    return render(request, 'teacher/dashboard.html', context)