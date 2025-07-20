from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserForm, StudentForm, TeacherForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    return render(request, 'home.html')


def register_student(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        student_form = StudentForm(request.POST)
        if user_form.is_valid() and student_form.is_valid():
            user = user_form.save()
            student = student_form.save(commit=False)
            student.user = user
            student.save()
            messages.success(request, "Student registered successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserForm()
        student_form = StudentForm()
    return render(request, 'register_student.html', {'user_form': user_form, 'student_form': student_form})


def register_teacher(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        teacher_form = TeacherForm(request.POST)
        if user_form.is_valid() and teacher_form.is_valid():
            user = user_form.save()
            teacher = teacher_form.save(commit=False)
            teacher.user = user
            teacher.save()
            messages.success(request, "Teacher registered successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserForm()
        teacher_form = TeacherForm()
    return render(request, 'register_teacher.html', {'user_form': user_form, 'teacher_form': teacher_form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')
            elif hasattr(user, 'student'):
                return redirect('dashboard')
            elif hasattr(user, 'teacher'):
                return redirect('dashboard')
            else:
                messages.error(request, "User role not recognized.")
                logout(request)
                return redirect('login')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    if hasattr(request.user, 'student'):
        return render(request, 'student_dashboard.html', {'student': request.user.student})
    elif hasattr(request.user, 'teacher'):
        return render(request, 'teacher_dashboard.html', {'teacher': request.user.teacher})
    else:
        messages.error(request, "No dashboard available for your user type.")
        return redirect('login')
