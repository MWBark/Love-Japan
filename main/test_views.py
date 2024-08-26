from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.test import TestCase
from .models import ImagePost, Profile, ImageComment
from .forms import ImageCommentForm, ProfileForm

# Create your tests here.
class TestMainViews(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(
        username="myUsername",
        email="test@test.com"
        )

        self.user.set_password('12345')
        self.user.save()


        self.imagepost = ImagePost(title="image title", uploader=self.user,
                                    slug="image-title", image="",
                                    message="message content", status=1)
        self.imagepost.save()

        
        profile = get_object_or_404(Profile, user=self.user)
        profile.bio = "something about me"
        profile.save()
        

    def test_render_homepage_logged_out(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"image title", response.content)
        self.assertIn(b"Login", response.content)


    def test_render_homepage_logged_in(self):
        self.client.login(username=self.user.username, password='12345')
        response = self.client.get(reverse('home'))
        self.assertIn(b"Logout", response.content)
        self.assertIn(b"navbar-brand", response.content)

    
    def test_render_imagepost(self):
        response = self.client.get(reverse(
            'imagepost', args=['image-title']))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"image title", response.content)
        self.assertIn(b"myUsername", response.content)
        self.assertIn(b"message content", response.content)
        self.assertIn(b"Created on", response.content)
        self.assertIsInstance(
            response.context['comment_form'], ImageCommentForm)

    def test_successful_image_comment_submission(self):
        """Test for posting a comment on a image post"""
        self.client.login(
            username="myUsername", password="12345")
        post_data = {
            'body': 'This is a test comment.'
        }
        response = self.client.post(reverse(
            'imagepost', args=["image-title"]), post_data, follow=True)
        self.assertRedirects(
            response, (reverse('imagepost', args=["image-title"])),
            status_code=302,
            target_status_code=200,
        )
        self.assertIn(
            b'Comment submitted and awaiting approval',
            response.content
        )

    def test_render_profilepage(self):
        response = self.client.get(reverse(
            'profile', args=["1"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"myUsername", response.content)
        self.assertIn(b"something about me", response.content)

    def test_render_profile_posts_page(self):
        response = self.client.get(reverse(
            'profile-posts', args=["1"]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"image title", response.content)

    def test_profile_page_profile_form(self):
        self.client.login(
            username="myUsername", password="12345")
        post_data = {
            'bio': 'Changed my bio'
        }
        response = self.client.post(reverse(
            'profile', args=["1"]), post_data, follow=True)
        self.assertRedirects(
            response, (reverse('profile', args=["1"])),
            status_code=302,
            target_status_code=200,
        )
        self.assertIn(b'Your Profile Has Been Updated!', response.content)
        self.assertIn(b'Changed my bio', response.content)
