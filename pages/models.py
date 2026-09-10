from django.db import models

# Create your models here.
from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.panels import FieldRowPanel

class MarketsPage(Page):
    """Салбарууд (Markets) хуудас"""
    intro = RichTextField(blank=True)

    content_panels  = Page.content_panels +[
        FieldPanel("intro"),
        InlinePanel("market_items", label="Салбар"),
    ]

    max_count = 1
    parent_page_types = ["home.HomePage"]

class MarketItem(Orderable):
    """Нэг салбар мэдээлэл"""
    page = ParentalKey(MarketsPage, on_delete=models.CASCADE, related_name="market_items")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Bootstrap Icon нэр, жишээ: building, cpu, lightning-charge"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("icon"),
    ]

class ServicesPage(Page):
    """Үйлчилгээ хуудас"""
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        InlinePanel("service_items", label="Үйлчилгээ"),
    ]

    max_count = 1
    parent_page_types = ["home.HomePage"]

class ServiceItem(Orderable):
    """Нэг үйлчилгээний мэдээлэл"""
    page = ParentalKey(ServicesPage, on_delete=models.CASCADE, related_name="service_items")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Bootstrap Icon нэр, жишээ: gear, briefcase, graph-up"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Expertise card-ын дэвсгэр зураг"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("icon"),
        FieldPanel("image"),
    ]

class ProjectsPage(Page):
    """Төслүүд хуудас"""
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        InlinePanel("project_items", label="Төсөл"),
    ]

    max_count = 1
    parent_page_types = ["home.HomePage"]

    def get_context(self, request):
        context = super().get_context(request)
        context["featured_items"] = self.project_items.filter(featured=True)
        context["categories"] = sorted(set(
            self.project_items.exclude(category="").values_list("category", flat=True)
        ))
        return context


class ProjectItem(Orderable):
    """Нэг төслийн мэдээлэл"""
    page = ParentalKey(ProjectsPage, on_delete=models.CASCADE, related_name="project_items")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True, help_text="Төслийн байршил")
    category = models.CharField(
        max_length=100,
        blank=True,
        help_text="Ж: Тээвэр, Эрчим хүч, Ус, Үл хөдлөх хөрөнгө, Дата төв"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Хуудасны эхэнд тодруулж харуулах эсэх"
    )
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    detail_page = models.ForeignKey(
        "pages.ProjectDetailPage",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Сонголтоор: энэ картыг дэлгэрэнгүй хуудас руу холбоно"
    )

    panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("location"),
        FieldPanel("category"),
        FieldPanel("featured"),
        FieldPanel("image"),
        FieldPanel("detail_page"),
    ]


class ProjectDetailPage(Page):
    """Нэг төслийн дэлгэрэнгүй (case-study) хуудас"""
    cover_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Хуудасны эхэн дэх бүтэн өргөн зураг"
    )
    location = models.CharField(max_length=255, blank=True)
    year = models.CharField(max_length=20, blank=True)
    status = models.CharField(
        max_length=50, blank=True,
        choices=[
            ("concept", "Санаа/Concept"),
            ("in_progress", "Хийгдэж байгаа"),
            ("completed", "Дууссан"),
        ],
        default="completed",
    )
    client = models.CharField(max_length=255, blank=True)
    intro = RichTextField(blank=True, help_text="Богино танилцуулга")
    body = RichTextField(blank=True, help_text="Дэлгэрэнгүй агуулга")

    content_panels = Page.content_panels + [
        FieldPanel("cover_image"),
        FieldRowPanel([
            FieldPanel("location"),
            FieldPanel("year"),
            FieldPanel("status"),
            FieldPanel("client"),
        ]),
        FieldPanel("intro"),
        FieldPanel("body"),
        InlinePanel("gallery_images", label="Галерейн зураг"),
    ]

    parent_page_types = ["pages.ProjectsPage"]

    def get_status_display_mn(self):
        return dict(self._meta.get_field("status").choices).get(self.status, self.status)

    def get_context(self, request):
        context = super().get_context(request)
        context["next_project"] = (
            ProjectDetailPage.objects.live()
            .sibling_of(self)
            .filter(path__gt=self.path)
            .order_by("path")
            .first()
            or ProjectDetailPage.objects.live().sibling_of(self).order_by("path").first()
        )
        return context


class ProjectGalleryImage(Orderable):
    """Төслийн дэлгэрэнгүй хуудасны галерейн нэг зураг"""
    page = ParentalKey(ProjectDetailPage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    caption = models.CharField(max_length=255, blank=True)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]


class NewsPage(Page):
    """Мэдээний жагсаалт харуулах хуудас"""
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    max_count = 1
    parent_page_types = ["home.HomePage"]
    subpage_types = ["pages.NewsArticlePage"]


class NewsArticlePage(Page):
    """Нэг мэдээний дэлгэрэнгүй хуудас"""
    date = models.DateField("Огноо")
    intro = models.CharField(max_length=500, blank=True, help_text="Жагсаалтад харагдах товч тайлбар")
    body = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    photographer_credit = models.CharField(
        max_length=255, blank=True,
        help_text="Ж: Зураг: Б.Бат"
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("intro"),
        FieldPanel("image"),
        FieldPanel("photographer_credit"),
        FieldPanel("body"),
    ]

    parent_page_types = ["pages.NewsPage"]

class AboutPage(Page):
    """Бидний тухай хуудас"""
    intro = RichTextField(blank=True)
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Судиогийн танилцуулга хэсгийн зураг"
    )
    mission = RichTextField(blank=True, help_text="Эрхэм зорилго")
    body = RichTextField(blank=True, help_text="Компанийн түүх, дэлгэрэнгүй танилцуулга")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("hero_image"),
        FieldPanel("mission"),
        FieldPanel("body"),
        InlinePanel("team_members", label="Багийн гишүүн"),
    ]

    max_count = 1
    parent_page_types = ["home.HomePage"]


class TeamMember(Orderable):
    """Багийн гишүүний мэдээлэл"""
    page = ParentalKey(AboutPage, on_delete=models.CASCADE, related_name="team_members")
    name = models.CharField(max_length=255, verbose_name="Нэр")
    position = models.CharField(max_length=255, blank=True, verbose_name="Албан тушаал")
    photo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("position"),
        FieldPanel("photo"),
    ]

class ContactPage(AbstractEmailForm):
    """Холбоо барих хуудас (маягттай)"""

    def get_form(self, *args, **kwargs):
        from django.forms.widgets import CheckboxInput

        form = super().get_form(*args, **kwargs)
        for field in form.fields.values():
            css_class = "form-check-input" if isinstance(field.widget, CheckboxInput) else "form-control"
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} {css_class}".strip()
        return form

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True, help_text="Маягт илгээсний дараа харагдах баярлалаа мессеж")

    address = models.CharField(max_length=255, blank=True, verbose_name="Хаяг")
    phone = models.CharField(max_length=100, blank=True, verbose_name="Утас")
    email = models.EmailField(blank=True, verbose_name="Имэйл")

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel("intro"),
        FieldPanel("address"),
        FieldPanel("phone"),
        FieldPanel("email"),
        InlinePanel("form_fields", label="Маягтын талбар"),
        FieldPanel("thank_you_text"),
        FieldRowPanel(
            [
                FieldPanel("from_address"),
                FieldPanel("to_address"),
            ]
        ),
        FieldPanel("subject"),
    ]

    max_count = 1
    parent_page_types = ["home.HomePage"]


class ContactFormField(AbstractFormField):
    page = ParentalKey(ContactPage, on_delete=models.CASCADE, related_name="form_fields")