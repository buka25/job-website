from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel


class HomePage(Page):
    statement = models.CharField(
        max_length=255, blank=True,
        default="Бид ирээдүйг илүү сайхан болгодог",
        help_text="Нүүр хуудасны хамгийн дээд, жижиг statement мөр"
    )
    hero_title = models.CharField(
        max_length=255,
        blank=True,
        default="Бид ирээдүйг хамтдаа бүтээж байна",
        help_text="Нүүр хуудасны гол гарчиг"
    )
    hero_subtitle = models.CharField(
        max_length=500,
        blank=True,
        default="Мэргэжлийн баг хамт олон, инновацийн шийдэл",
        help_text="Гарчигийн доорх богино тайлбар"
    )
    hero_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Hero хэсэгт харагдах том зураг"
    )
    intro_heading = models.CharField(max_length=255, blank=True, default="Бидний тухай")
    intro_text = RichTextField(blank=True)
    story_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="'Бидний тухай' хэсэгт харагдах том зураг"
    )

    years_heading = models.CharField(
        max_length=255, blank=True,
        default="Бид олон жилийн турш ирээдүйг илүү сайхан болгож ирсэн"
    )

    people_heading = models.CharField(max_length=255, blank=True, default="Манай хамт олон")
    people_subheading = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("statement"),
        FieldPanel("hero_title"),
        FieldPanel("hero_subtitle"),
        FieldPanel("hero_image"),
        FieldPanel("intro_heading"),
        FieldPanel("intro_text"),
        FieldPanel("story_image"),
        FieldPanel("years_heading"),
        InlinePanel("idea_cards", label="Карт (Our story/Careers г.м)"),
        FieldPanel("people_heading"),
        FieldPanel("people_subheading"),
        InlinePanel("people_cards", label="Хүн"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        from jobs.models import JobPage
        context["latest_jobs"] = JobPage.objects.live().order_by("-first_published_at")[:3]
        return context


class IdeaCard(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="idea_cards")
    tag = models.CharField(max_length=50, blank=True, help_text="Ж: About, Careers")
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True, help_text="Ж: /about/")
    image = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        FieldPanel("tag"),
        FieldPanel("title"),
        FieldPanel("description"),
        FieldPanel("link"),
        FieldPanel("image"),
    ]


class PeopleCard(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name="people_cards")
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    quote = models.TextField(blank=True)
    photo = models.ForeignKey(
        "wagtailimages.Image", null=True, blank=True,
        on_delete=models.SET_NULL, related_name="+"
    )

    panels = [
        FieldPanel("name"),
        FieldPanel("role"),
        FieldPanel("quote"),
        FieldPanel("photo"),
    ]