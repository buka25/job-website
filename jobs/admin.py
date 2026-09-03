from django.contrib import admin

from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("full_name", "job", "email", "phone", "submitted_at")
    list_filter = ("job",)
    search_fields = ("full_name", "email", "phone")
    readonly_fields = ("job", "full_name", "email", "phone", "cover_letter", "resume", "submitted_at")
