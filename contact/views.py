from django.shortcuts import render
from .models import ContactInfo


def contact(request):
    """
    Renders the most recent contact information
    by displaying an individual instance of :model:`contact:ContactInfo`.
    """

    contact_info = ContactInfo.objects.all().order_by('-updated_on').first()

    return render(request, "contact/contact.html", {"contact_info": contact_info})
