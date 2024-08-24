from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.test import TestCase
from .models import ImagePost, Profile, ImageComment

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

        self.imagecomment = ImageComment(imagepost=self.imagepost, author=self.user,
                                        body="Nice", status=1)
        self.imagecomment.save()

        
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
        self.assertIn(b"Nice", response.content)

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
