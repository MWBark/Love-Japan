from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from .models import ImagePost

# Create your tests here.
class TestMainViews(TestCase):

        def setUp(self):
            self.user = User.objects.create_superuser(
            username="myUsername",
            password="myPassword",
            email="test@test.com"
            )

            self.imagepost = ImagePost(title="image title", uploader=self.user,
                         slug="image-title", image="",
                         message="image content", status=1)
            self.imagepost.save()
        
        def test_render_homepage(self):
            response = self.client.get(reverse('home'))
            self.assertEqual(response.status_code, 200)