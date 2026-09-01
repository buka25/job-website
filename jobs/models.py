from django.db import models

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