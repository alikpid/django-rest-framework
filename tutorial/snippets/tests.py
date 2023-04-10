from django.test import TestCase
from snippets.models import Snippet
from django.contrib.auth.models import User


class SnippetModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser',
                                             password='testpass',
                                             email='test@example.com')
        self.snippet = Snippet.objects.create(owner=self.user,
                                              title='Test Snippet',
                                              code='Very useful code snippet',
                                              linenos=True,
                                              language='python',
                                              style='friendly')

    def test_snippet_creation(self):
        self.assertEqual(Snippet.objects.count(), 1)
        self.assertEqual(self.snippet.title, 'Test Snippet')
        self.assertEqual(self.snippet.code, 'Very useful code snippet')
        self.assertEqual(self.snippet.linenos, True)
        self.assertEqual(self.snippet.language, 'python')
        self.assertEqual(self.snippet.style, 'friendly')
        self.assertEqual(self.snippet.owner, self.user)

    def test_snippet_updating(self):
        self.snippet.title = 'Edited Snippet'
        self.snippet.save()
        self.assertEqual(self.snippet.title, 'Edited Snippet')

    def test_snippet_deletion(self):
        self.snippet.delete()
        self.assertEqual(Snippet.objects.count(), 0)