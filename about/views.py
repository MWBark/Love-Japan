from django.shortcuts import render
from .models import About


def about(request):
    """
    Renders the most recent information about the site
    by displaying an individual instance of :model:`about:About`.
    """

    about = About.objects.all().order_by('-updated_on').first()

    return render(request, "about/about.html", {"about": about})
