from django.db import models
from django.shortcuts import redirect
from django.template.response import TemplateResponse

# Create your models here.
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel

class JobIndexPage(Page):
    """Бүх ажлын зарын жагсаалт харуулах хуудас"""
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ["jobs.JobPage"]


class JobPage(Page):
    """Нэг ажлын зарын дэлгэрэнгүй хуудас"""
    location = models.CharField(max_length=255, blank=True)
    salary = models.CharField(max_length=255, blank=True, help_text="Ж: 1,500,000 - 2,000,000₮")
    employment_type = models.CharField(
        max_length=50,
        choices=[
            ("full_time", "Бүтэн цагийн"),
            ("part_time", "Хагас цагийн"),
            ("remote", "Зайнаас"),
        ],
        default="full_time",
    )
    description = RichTextField(blank=True)
    requirements = RichTextField(blank=True, help_text="Тавигдах шаардлага")
    deadline = models.DateField(blank=True, null=True, help_text="Өргөдөл хүлээн авах эцсийн хугацаа")

    content_panels = Page.content_panels + [
        FieldPanel("location"),
        FieldPanel("salary"),
        FieldPanel("employment_type"),
        FieldPanel("description"),
        FieldPanel("requirements"),
        FieldPanel("deadline"),
    ]

    parent_page_types = ["jobs.JobIndexPage"]

    def serve(self, request, *args, **kwargs):
        from .forms import JobApplicationForm

        submitted = False
        if request.method == "POST":
            form = JobApplicationForm(request.POST, request.FILES)
            if form.is_valid():
                application = form.save(commit=False)
                application.job = self
                application.save()
                return redirect(self.url + "?submitted=1")
        else:
            form = JobApplicationForm()
            submitted = request.GET.get("submitted") == "1"

        context = self.get_context(request)
        context["application_form"] = form
        context["application_submitted"] = submitted
        return TemplateResponse(request, self.get_template(request), context)


class JobApplication(models.Model):
    """Ажлын байранд ирсэн өргөдөл"""
    job = models.ForeignKey(JobPage, on_delete=models.CASCADE, related_name="applications")
    full_name = models.CharField(max_length=255, verbose_name="Овог нэр")
    email = models.EmailField(verbose_name="Имэйл")
    phone = models.CharField(max_length=50, verbose_name="Утас")
    cover_letter = models.TextField(blank=True, verbose_name="Танилцуулга")
    resume = models.FileField(upload_to="applications/%Y/%m/", verbose_name="CV / Резюме")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = "Өргөдөл"
        verbose_name_plural = "Өргөдлүүд"

    def __str__(self):
        return f"{self.full_name} — {self.job.title}"