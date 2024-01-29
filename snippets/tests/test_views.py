import io

from django import shortcuts
from django.test import Client, TestCase
from rest_framework.parsers import JSONParser

from snippets.models import SimpleSnippet


class ViewFunctionTest(TestCase):
    client = Client()

    def test_json_response(self):
        """
            http http://127.0.0.1:8000/json/
        """
        address = shortcuts.reverse("json_response")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        data = JSONParser().parse(content_reader)
        self.assertIn("greeting", data)


    def test_json_snippet_list(self):
        """
            http http://127.0.0.1:8000/json_snippets/
        """
        code = "hello world"
        snippet = SimpleSnippet.objects.create(code=code)

        address = shortcuts.reverse("django_style_snippet_list")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        data = JSONParser().parse(content_reader)
        correct_snippet_json = {'id': 1, 'code': 'hello world'}
        self.assertIn(correct_snippet_json, data)

        snippet.delete()

    def test_json_snippet_detail(self):
        """
            http http://127.0.0.1:8000/json_snippets/1
        """
        code = "hello world"
        snippet = SimpleSnippet.objects.create(code=code)

        address = shortcuts.reverse("django_style_snippet_detail", kwargs={"pk": 1})
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        data = JSONParser().parse(content_reader)
        self.assertIn("code", data)

        snippet.delete()