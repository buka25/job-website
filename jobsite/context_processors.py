def footer_contact(request):
    from pages.models import ContactPage

    return {"footer_contact_page": ContactPage.objects.live().first()}
