from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.utils.text import slugify
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views import generic
from PIL import Image
from taggit.models import Tag
from .models import ImagePost, Profile, ImageComment, Notification
from .forms import ProfileForm, UploadImageForm, ImageCommentForm


def is_valid_image_pillow(file_name):
    try:
        with Image.open(file_name) as img:
            img.verify()
            return True
    except (IOError, SyntaxError):
        return False


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
            messages.error(request, 'Error uploading comment!')

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
    """
    Edit an individual :model:`main.ImagePost`.

    **Context**

    ``imagepost``
        An instance of :model:`main.ImagePost`.
    ``upload_image_form``
        An instance of :form:`main.UploadImageForm`.

    **Template:**

    :template:`main/uploadimage.html`
    """

    queryset = ImagePost.objects.prefetch_related('tags').all()
    imagepost = get_object_or_404(queryset, slug=slug)
    upload_image_form = UploadImageForm(request.POST or None, request.FILES or None, instance=imagepost)

    if request.user == imagepost.uploader:   
        if request.method == "POST":
            if upload_image_form.is_valid():
                new_imagepost = upload_image_form.save(commit=False)
                if is_valid_image_pillow(new_imagepost.image):
                    new_imagepost.uploader = request.user
                    new_imagepost.slug = slugify(imagepost.title)
                    new_imagepost.status = 0
                    new_imagepost.save()
                    upload_image_form.save_m2m()
                    messages.success(request, ("Your Image has been update and is awaiting approval."))
                else:
                    messages.error(request, 'Not a valid image file!')
                    return redirect('imagepost_edit', slug)
                return redirect('home')
            else:
                messages.error(request, 'Error updating image!')
    else:
        messages.error(request, "You don't have permission to edit this post!")
        return redirect('imagepost', slug)

    return render(request, 'main/uploadimage.html', {"imagepost":imagepost, "upload_image_form":upload_image_form})

def imagepost_delete(request, slug):
    """
    Delete an individual :model:`main.ImagePost`.

    **Context**

    ``imagepost``
        An instance of :model:`main.ImagePost`.
    """

    queryset = ImagePost.objects.all()
    imagepost = get_object_or_404(queryset, slug=slug)

    if imagepost.uploader == request.user:
        imagepost.delete()
        messages.success(request, 'Image deleted!')
    else:
        messages.error(request, 'You can only delete your own Images!')

    return HttpResponseRedirect(reverse('home'))

def imagepost_like(request, slug):
    """
    Add or remove request :model:`auth.User` to
    the 'likes' attribute of :model:`main.ImagePost`

    **Context**

    ``imagepost``
        An instance of :model:`main.ImagePost`.
    """
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
        messages.error(request, 'You must be logged in to like.')
        return redirect('imagepost', slug)



def comment_edit(request, slug, comment_id):
    """
    Allows an authorized user to edit thier :model:`main.ImageComment`

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
            messages.success(request, 'Comment Updated!')
        else:
            messages.error(request, 'Error updating comment!')

    return HttpResponseRedirect(reverse('imagepost', args=[slug]))


def comment_delete(request, slug, comment_id):
    """
    Delete an individual :model:`main.ImageComment`

    **Content**

    ``imagepost``
        An instance of :model:`main.ImagePost`.
    ``comment``
        A single image comment related to a image post.
    """
    queryset = ImagePost.objects.filter(status=1)
    imagepost = get_object_or_404(queryset, slug=slug)
    comment = get_object_or_404(ImageComment, pk=comment_id)

    if comment.author == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted!')
    else:
        messages.error(request, 'You can only delete your own comments!')

    return HttpResponseRedirect(reverse('imagepost', args=[slug]))


def comment_like(request, slug, comment_id):
    """
    Add or remove request :model:`auth.User` to
    the 'likes' attribute of :model:`main.ImageComment`

    **Content**

    ``imagepost``
        An instance of :model:`main.ImagePost`.
    ``comment``
        A single image comment related to a image post.
    """
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
        messages.error(request, 'You must be logged in to like.')
        return redirect('imagepost', slug)


def profile(request, pk):
    """
    Page related to a registered user's :model:`main.Profile`.

    **Content**

    ``profile``
        An instance of :model:`main.Profile`.
    ``profile_images``
        All :model:`main.ImagePosts`related to profile.
    ``profile_form``
        An instance of :form:`main.ProfileForm`.

    **Templates**

    :template:`main/profile.html`
    """
    queryset = Profile.objects.all()
    profile = get_object_or_404(queryset, user_id=pk)
    approved_images = ImagePost.objects.filter(uploader=pk, status=1)
    draft_images = ImagePost.objects.filter(uploader=pk, status=0)
    profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)

    if request.method == "POST":
        if profile_form.is_valid() and profile.user == request.user:
            new_profile = profile_form.save(commit=False)
            if is_valid_image_pillow(new_profile.image):
                new_profile.save()
                messages.success(request, ("Your Profile Has Been Updated!"))
                return HttpResponseRedirect(reverse('profile', args=[pk]))
            else:
                messages.error(request, 'Not a valid image file!')
                return redirect('profile', pk)
        else:
            messages.error(request, 'Error updating profile image!')

    return render(
        request, 
        'main/profile.html', 
        {
            "profile":profile, 
            "approved_images":approved_images, 
            "draft_images":draft_images,
            "profile_form":profile_form
        }
    )


class ProfilePostList(generic.ListView):
    """
    Uses django's generic.Listview to filter approved imageposts
    related to a user profile and to paginate posts by 8 per page.
    """
    queryset = ImagePost.objects.filter(status=1)
    template_name = "main/index.html"
    paginate_by = 8

    def get_queryset(self):
        """return all ImagePosts by uploader==primary key"""
        return ImagePost.objects.filter(uploader=self.kwargs.get('pk'), status=1)


def profile_drafts(request, pk):

    profile = Profile.objects.get(user_id=pk)
    if request.user == profile.user:
        imagepost_list = ImagePost.objects.filter(uploader=profile.user, status=0)

        paginator = Paginator(imagepost_list, 8)  # Show 8 images per page.
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
    else:
        messages.error(request, "You don't have permission to view this page")
        return redirect('home')

    return render(
        request,
        'main/index.html',
        {
            "imagepost_list":imagepost_list,
            "page_obj":page_obj
        }
    )


class TagPostList(generic.ListView):
    """
    Uses django's generic.Listview to filter approved imageposts
    related to a :model:`taggit.Tag` and to paginate posts by 8 per page.
    """
    queryset = ImagePost.objects.filter(status=1)
    template_name = "main/index.html"
    paginate_by = 8

    def get_queryset(self):
        """return all ImagePosts by tags==tag"""
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return ImagePost.objects.filter(tags=tag)


def taglist(request):
    """
    Render list of all :model:`taggit.Tag`.

    **Content**

    ``tags``
        all tags

    **Templates**

    :template:`main/tags.html`
    """

    tags = Tag.objects.all()

    return render(request, 'main/tags.html', {"tags":tags})


def upload_image(request):
    """
    Create a :model:`main.Imagepost`

    **content**

    ``upload_image_form``
        an instance of :form:`main.UploadImageForm`.

    **Templates**

    :template:`main/uploadimage.html.html`
    """
    upload_image_form = UploadImageForm(request.POST or None, request.FILES or None)

    if request.method == "POST":
        if upload_image_form.is_valid():
            imagepost = upload_image_form.save(commit=False)
            if is_valid_image_pillow(imagepost.image):
                imagepost.uploader = request.user
                imagepost.slug = slugify(imagepost.title)
                imagepost.save()
                upload_image_form.save_m2m()
                messages.success(request, ("Your Image is awaiting approval."))
                return redirect('home')
            else:
                messages.error(request, 'Not a valid image file!')
                return redirect('upload_image')
        else:
            messages.error(request, 'Error uploading image!')

    return render(request, 'main/uploadimage.html', {"upload_image_form":upload_image_form})

def notifications(request):
    """
    Gets all :model:`main.Notification` related to
    request user where its attribute is_read = True
    and orders newest first

    **Content**

    ``read_notifications``
        all notifications related to user where is_read=True

    **Templates**

    :template:`main/notifications.html`.
    """

    read_notifications = Notification.objects.filter(user=request.user, is_read=True).order_by('-created_on')

    return render(request, 'main/notifications.html', {"read_notifications":read_notifications})


def notification_is_read(request, n_id):
    """
    Sets :model:`main.Notification` attribute is_read = True

    **Content**

    ``notification``
        instance of :model:`main.Notification` 
    """
    queryset = Notification.objects.filter(is_read=False)
    notification = get_object_or_404(queryset, pk=n_id)

    if notification.user == request.user:
        notification.is_read = True
        notification.save()
        messages.success(request, ("Notification marked as read."))
        return HttpResponseRedirect(reverse('notifications'))
    else:
        messages.error(request, 'Error updating notification!')
        return redirect('notifications')


def search(request):

    if request.method == 'POST':
        searched = request.POST['searched']
        search_slug = slugify(searched)
        imageposts = ImagePost.objects.filter(slug__contains=search_slug)
        paginator = Paginator(imageposts, 8)  # Show 8 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'main/search.html', {"searched":searched, "imageposts":imageposts, "page_obj": page_obj})


def handler403(request, exception):
    """Render custom :template:`main/403.html` for 403 error"""
    return render(request, 'main/403.html', status=403)


def handler404(request, exception):
    """Render custom :template:`main/404.html` for 404 error"""
    return render(request, 'main/404.html', status=404)


def handler500(request):
    """Render custom :template:`main/500.html` for 500 error"""
    return render(request, 'main/500.html', status=500)



        
