from django.test import TestCase
from .forms import ImageCommentForm


class TestImageCommentForm(TestCase):

    def test_form_is_valid(self):
        comment_form = ImageCommentForm({'body': 'This is a great post!'})
        self.assertTrue(comment_form.is_valid(), msg='Form is not valid')

    def test_form_is_invalid(self):
        comment_form = ImageCommentForm({'body': ''})
        self.assertFalse(comment_form.is_valid(), msg='Form is valid')
