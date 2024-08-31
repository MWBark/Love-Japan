from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.utils.text import slugify
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import generic
from taggit.models import Tag
from .models import ImagePost, Profile, ImageComment, Notification
from .forms import ProfileForm, UploadImageForm, ImageCommentForm


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
    ``image_comments``
        All comments related to imagepost

    **Template:**

    :template:`main/imagepost.html`
    """
    queryset = ImagePost.objects.prefetch_related('tags').all()
    imagepost = get_object_or_404(queryset, slug=slug)
    image_comments = ImageComment.objects.filter(imagepost=imagepost).order_by("-created_on")

    if request.method == "POST":
        comment_form = ImageCommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.imagepost = imagepost
            comment.save()
            messages.success(request, ('Comment submitted and awaiting approval'))
            return HttpResponseRedirect(reverse('imagepost', args=[slug]))
        else:
            messages.add_message(request, messages.ERROR, 'Error updating profile image!')

    comment_form = ImageCommentForm()
    
    return render(
        request,
        'main/imagepost.html',
        {
            "imagepost":imagepost,
            "image_comments":image_comments,
            "comment_form":comment_form,
        }
    )


def imagepost_edit(request, slug):

    queryset = ImagePost.objects.prefetch_related('tags').all()
    imagepost = get_object_or_404(queryset, slug=slug)
    upload_image_form = UploadImageForm(request.POST or None, request.FILES or None, instance=imagepost)

    if request.method == "POST":
        if upload_image_form.is_valid():
            imagepost = upload_image_form.save(commit=False)
            imagepost.uploader = request.user
            imagepost.slug = slugify(imagepost.title)
            imagepost.status = 0
            imagepost.save()
            upload_image_form.save_m2m()
            messages.success(request, ("Your Image has been update and is awaiting approval."))
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Error uploading image!')

    return render(request, 'main/uploadimage.html', {"imagepost":imagepost, "upload_image_form":upload_image_form})

def imagepost_delete(request, slug):

    queryset = ImagePost.objects.all()
    imagepost = get_object_or_404(queryset, slug=slug)

    if imagepost.uploader == request.user:
        imagepost.delete()
        messages.add_message(request, messages.SUCCESS, 'Image deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own Images!')

    return HttpResponseRedirect(reverse('home'))

def imagepost_like(request, slug):
    if request.user.is_authenticated:
        queryset = ImagePost.objects.all()
        imagepost = get_object_or_404(queryset, slug=slug)

        if imagepost.likes.filter(id=request.user.id):
            imagepost.likes.remove(request.user)
            messages.success(request, ("Removed like from image."))
        else:
            imagepost.likes.add(request.user)
            messages.success(request, ("Added like to comment."))

        return HttpResponseRedirect(reverse('imagepost', args=[slug]))
    else:
        messages.add_message(request, messages.ERROR, 'You must be logged in to like.')
        return redirect('imagepost', slug)



def comment_edit(request, slug, comment_id):
    """
    Allows an authorized user to edit thier :model:`main.comment`

    **Content**

    ``imagepost``
        An instance of :model:`main.ImagePost`.
    ``comment``
        A single comment related to a post.
    ``comment_form``
        An instance of :form:`main.ImageCommentForm`.
    """
    if request.method == "POST":

        queryset = ImagePost.objects.filter(status=1)
        imagepost = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(ImageComment, pk=comment_id)
        comment_form = ImageCommentForm(data=request.POST, instance=comment)

        if comment_form.is_valid() and comment.author == request.user:
            comment = comment_form.save(commit=False)
            comment.imagepost = imagepost
            comment.approved = False
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Comment Updated!')
        else:
            messages.add_message(request, messages.ERROR, 'Error updating comment!')

    return HttpResponseRedirect(reverse('imagepost', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    Delete an individual comment

    **Content**

    ``post``
        An instance of :model:`main.ImagePost`.
    ``comment``
        A single image comment related to a image post.
    """
    queryset = ImagePost.objects.filter(status=1)
    imagepost = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(ImageComment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, 'Comment deleted!')
    else:
        messages.add_message(request, messages.ERROR, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('imagepost', args=[slug]))


def comment_like(request, slug, comment_id):

    if request.user.is_authenticated:
        queryset = ImagePost.objects.filter(status=1)
        imagepost = get_object_or_404(queryset, slug=slug)
        comment = get_object_or_404(ImageComment, pk=comment_id)

        if comment.likes.filter(id=request.user.id):
            comment.likes.remove(request.user)
            messages.success(request, ("Removed like from comment."))
        else:
            comment.likes.add(request.user)
            messages.success(request, ("Added like to comment."))

        return HttpResponseRedirect(reverse('imagepost', args=[slug]))
    else:
        messages.add_message(request, messages.ERROR, 'You must be logged in to like.')
        return redirect('imagepost', slug)


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
    queryset = ImagePost.objects.filter(status=1)
    template_name = "main/index.html"
    paginate_by = 8

    def get_queryset(self):
        """return all ImagePosts by uploader==primary key"""
        return ImagePost.objects.filter(uploader=self.kwargs.get('pk'))


class TagPostList(generic.ListView):
    queryset = ImagePost.objects.filter(status=1)
    template_name = "main/index.html"
    paginate_by = 8

    def get_queryset(self):
        """return all ImagePosts by tags==tag"""
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return ImagePost.objects.filter(tags=tag)


def upload_image(request):
    upload_image_form = UploadImageForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if upload_image_form.is_valid():
            imagepost = upload_image_form.save(commit=False)
            imagepost.uploader = request.user
            imagepost.slug = slugify(imagepost.title)
            imagepost.save()
            upload_image_form.save_m2m()
            messages.success(request, ("Your Image is awaiting approval."))
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Error uploading image!')

    return render(request, 'main/uploadimage.html', {"upload_image_form":upload_image_form})

def notifications(request):

    read_notifications = Notification.objects.filter(user=request.user, is_read=True).order_by('-created_on')

    return render(request, 'main/notifications.html', {"read_notifications":read_notifications})


def notification_is_read(request, n_id):

    queryset = Notification.objects.filter(is_read=False)
    notification = get_object_or_404(queryset, pk=n_id)

    if notification.user == request.user:
        notification.is_read = True
        notification.save()
        messages.success(request, ("Notification marked as read."))
        return HttpResponseRedirect(reverse('notifications'))
    else:
        messages.add_message(request, messages.ERROR, 'Error updating notification!')
        return redirect('notifications')
