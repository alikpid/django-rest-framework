import json
import unittest
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIRequestFactory
from rest_framework.request import Request
from snippets.views import SnippetViewSet


# class SnippetModelTestCase(TestCase):
#     def setUp(self):
#         self.user = User.objects.create_user(username='testuser',
#                                              password='testpass',
#                                              email='test@example.com')
#         self.snippet = Snippet.objects.create(owner=self.user,
#                                               title='Test Snippet',
#                                               code='Very useful snippet code',
#                                               linenos=True,
#                                               language='python',
#                                               style='friendly')
#
#     def test_snippet_creation(self):
#         self.assertEqual(Snippet.objects.count(), 1)
#         self.assertEqual(self.snippet.title, 'Test Snippet')
#         self.assertEqual(self.snippet.code, 'Very useful snippet code')
#         self.assertEqual(self.snippet.linenos, True)
#         self.assertEqual(self.snippet.language, 'python')
#         self.assertEqual(self.snippet.style, 'friendly')
#         self.assertEqual(self.snippet.owner, self.user)
#
#     def test_snippet_updating(self):
#         self.snippet.title = 'Edited Snippet'
#         self.snippet.save()
#         self.assertEqual(self.snippet.title, 'Edited Snippet')
#
#     def test_snippet_deletion(self):
#         self.snippet.delete()
#         self.assertEqual(Snippet.objects.count(), 0)


class SnippetViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.snippet1 = Snippet.objects.create(owner=self.user,
                                               title='test snippet 1',
                                               code='Very useful snippet code',
                                               language='python')

        self.snippet2 = Snippet.objects.create(owner=self.user,
                                               title='test snippet 2',
                                               code='Very very useful snippet code',
                                               language='python')

    def test_snippet_list(self):
        url = reverse('snippet-list')
        request = APIRequestFactory().get(url)
        response = self.client.get(url, format='json')
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True, context={'request': request})

        expected_data = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': serializer.data
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.dumps(response.data, sort_keys=True), json.dumps(expected_data, sort_keys=True))

    def test_create_snippet(self):
        url = reverse('snippet-list')
        data = {
            'title': 'new test snippet',
            'code': 'Very aaa useful snippet code',
            'language': 'python'
        }
        request = APIRequestFactory().post(url, data, format='json')
        request.user = self.user
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)