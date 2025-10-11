from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ThesisUploadForm
from .models import Thesis

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.user_type == 'student':
                return redirect('student_dashboard')
            elif user.user_type == 'supervisor':
                return redirect('supervisor_dashboard')
            elif user.user_type == 'admin':
                return redirect('admin_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')



def student_dashboard(request):
    theses = Thesis.objects.filter(student=request.user)
    return render(request, 'dashboard_student.html', {'theses': theses})

def supervisor_dashboard(request):
    theses = Thesis.objects.filter(supervisor=request.user)
    return render(request, 'dashboard_supervisor.html', {'theses': theses})

def upload_thesis(request):
    if request.method == 'POST':
        form = ThesisUploadForm(request.POST, request.FILES)
        if form.is_valid():
            thesis = form.save(commit=False)
            thesis.student = request.user
            thesis.save()
            return redirect('student_dashboard')
    else:
        form = ThesisUploadForm()
    return render(request, 'upload_thesis.html', {'form': form})

