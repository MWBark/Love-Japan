from django.shortcuts import render, reverse, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import generic
from .models import ImagePost, Profile
from .forms import ProfileForm


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


def profile(request, pk):
    profile = Profile.objects.get(user_id=pk)
    profile_images = ImagePost.objects.filter(uploader=pk)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == "POST":
        if profile_form.is_valid() and profile.user == request.user:
            profile_form.save()
            messages.success(request, ("Your Profile Has Been Updated!"))
            return HttpResponseRedirect(reverse('profile', args=[pk]))
        else:
            messages.add_message(request, messages.ERROR, 'Error updating profile image!')

    return render(
        request, 
        'main/profile.html', 
        {
            "profile":profile, 
            "profile_images":profile_images, 
            "profile_form":profile_form
        }
    )


class ProfilePostList(generic.ListView):
    queryset = ImagePost.objects.all()
    template_name = "main/index.html"
    paginate_by = 8

    def get_queryset(self):
        """return all ImagePosts by uploader==primary key"""
        return ImagePost.objects.filter(uploader=self.kwargs.get('pk'))
