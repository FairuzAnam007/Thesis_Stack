from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import StudentProfile, ThesisGroup, ThesisSubmission

admin.site.register(StudentProfile)
admin.site.register(ThesisGroup)
admin.site.register(ThesisSubmission)
