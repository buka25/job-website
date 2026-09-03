from django import forms

from .models import JobApplication


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ["full_name", "email", "phone", "cover_letter", "resume"]
        labels = {
            "full_name": "Овог нэр",
            "email": "Имэйл",
            "phone": "Утас",
            "cover_letter": "Танилцуулга",
            "resume": "CV / Резюме (PDF, Word)",
        }
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "cover_letter": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def clean_resume(self):
        resume = self.cleaned_data["resume"]
        allowed_extensions = (".pdf", ".doc", ".docx")
        if not resume.name.lower().endswith(allowed_extensions):
            raise forms.ValidationError("Зөвхөн PDF эсвэл Word файл хавсаргана уу.")
        max_size_mb = 5
        if resume.size > max_size_mb * 1024 * 1024:
            raise forms.ValidationError(f"Файлын хэмжээ {max_size_mb}MB-с хэтрэхгүй байх ёстой.")
        return resume
