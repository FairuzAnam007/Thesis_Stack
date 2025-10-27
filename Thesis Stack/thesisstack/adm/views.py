from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from main.models import User
from accounts.models import StudentProfile
from faculty.models import FacultyProfile
from .models import AdminProfile
from .forms import (AdminLoginForm,UserEditForm,StudentProfileAdminForm,FacultyProfileAdminForm)

def admin_login(request):
    if request.user.is_authenticated and request.user.role == "admin":
        return redirect("admin_dashboard")

    if request.method == "POST":
        form = AdminLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.role != "admin":
                messages.error(request, "Access denied. Only admins can log in here.")
                return redirect("admin_login")
            login(request, user)
            messages.success(request, f"Welcome, {user.first_name or user.username}!")
            return redirect("admin_dashboard")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AdminLoginForm()

    return render(request, "login.html", {"form": form})


def admin_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")


@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")

    profile, _ = AdminProfile.objects.get_or_create(
        user=request.user,
        defaults={"department": "CSE", "designation": "Department Admin"},
    )

    total_students = StudentProfile.objects.count()
    total_faculty = FacultyProfile.objects.count()

    return render(
        request,
        "adm_dashboard.html",
        {
            "profile": profile,
            "total_students": total_students,
            "total_faculty": total_faculty,
        },
    )

