from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignUpForm, ThesisUploadForm
from .models import Thesis
from django.contrib import messages
from django.shortcuts import render
from accounts.models import StudentProfile, ThesisGroup
from faculty.models import FacultyProfile, Supervision
from profiles.models import UserProfile


def home(request):
    context = {}
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user).first()
        context['profile'] = profile

        if request.user.role == 'student':
            group = ThesisGroup.objects.filter(members=request.user).first()
            supervision = Supervision.objects.filter(group=group).first()
            context['thesis_group'] = group
            context['supervision'] = supervision


        elif request.user.role == 'supervisor':
            faculty = FacultyProfile.objects.filter(user=request.user).first()
            context['faculty'] = faculty

    return render(request, 'home.html', context)
