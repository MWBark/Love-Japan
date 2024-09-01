from django.shortcuts import render, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import ContactInfo
from .forms import ContactForm


def contact(request):
    """
    Renders the most recent contact information
    by displaying an individual instance of :model:`contact.ContactInfo`
    and allows users to send a contact message with :form:`contact.ContactForm`

    **Content**

    ``contact_info``
        instance of :model:`contact.ContactInfo`
    ``contact_form``
        instance of :form:`contact.ContactForm`

    **Templates**

    :template:`contact/contact.html`
    """

    contact_info = ContactInfo.objects.all().order_by('-updated_on').first()

    if request.method == "POST":
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact = contact_form.save(commit=False)
            if request.user.is_authenticated:
                contact.username = request.user.username
            contact.save()
            messages.success(request, ("Message sent! We'll get back to you ASAP."))
            return HttpResponseRedirect(reverse('contact'))
        else:
            messages.error(request, 'Error sending message!')

    contact_form = ContactForm()

    return render(request, "contact/contact.html", {"contact_info": contact_info, "contact_form":contact_form})
