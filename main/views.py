from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import ImagePost


# Create your views here.
class ImagePostList(generic.ListView):
    """
    Uses django's generic.Listview to filter approved imageposts
    and to paginate posts by 8 per page.
    """
    queryset = ImagePost.objects.filter(status=1)
    template_name = "main/index.html"
    paginate_by = 8


def imagepost(request, slug):
    """
    Display an individual :model:`main.ImagePost`.

    **Context**

    ``imagepost``
        An instance of :model:`main.ImagePost`.

    **Template:**

    :template:`main/imagepost.html`
    """
    queryset = ImagePost.objects.filter(status=1)
    imagepost = get_object_or_404(queryset, slug=slug)
    return render(request, 'main/imagepost.html', {"imagepost":imagepost})