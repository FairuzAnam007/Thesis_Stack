from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ThesisGroup, ThesisSubmission, StudentProfile
from .forms import ThesisGroupForm, ThesisSubmissionForm, StudentLoginForm , StudentProfileForm
from faculty.models import Supervision
from main.models import Feedback

def student_login(request):
    storage = messages.get_messages(request)
    for _ in storage:
        pass
    if request.user.is_authenticated:
        if request.user.role == 'student':
            return redirect('student_dashboard')
        elif request.user.role == 'supervisor':
            return redirect('faculty_dashboard')
    if request.method == "POST":
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.role == 'student':
                return redirect('student_dashboard')
            elif user.role == 'supervisor':
                return redirect('faculty_dashboard')
            else:
                messages.error(request, "Invalid role. Contact admin.")
                return redirect('student_login')
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = StudentLoginForm()
    return render(request, 'login.html', {'form': form})

def student_logout(request):
    logout(request)
    return redirect('home')

@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('home')

    profile = StudentProfile.objects.filter(user=request.user).first()
    user_profile = None
    from profiles.models import UserProfile
    user_profile = UserProfile.objects.filter(user=request.user).first()

    groups = ThesisGroup.objects.filter(members=request.user) | ThesisGroup.objects.filter(creator=request.user)
    groups = groups.distinct()
    submissions = ThesisSubmission.objects.filter(student=request.user)


    return render(request, 'dashboard.html', {
        'profile': profile,
        'user_profile': user_profile,
        'groups': groups,

    })