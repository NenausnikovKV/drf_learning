import io
import json
from collections import OrderedDict

from django import shortcuts
from django.test import Client, TestCase
from rest_framework.parsers import JSONParser

from snippets.models import SimpleSnippet


class DjangoStyleViewFunctionTest(TestCase):
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
        correct_response_data = {'id': 1, 'code': 'hello world'}
        self.assertEquals(data, correct_response_data)

        snippet.delete()


class DRFStyleFunctionView(TestCase):
    client = Client()

    def test_json_snippet_list(self):
        """
            http http://127.0.0.1:8000/simple_snippets/

            http http://127.0.0.1:8000/simple_snippets/ Accept:application/json
            http http://127.0.0.1:8000/simple_snippets.json


            http http://127.0.0.1:8000/simple_snippets/ Accept:text/html
            http http://127.0.0.1:8000/simple_snippets.api

            http --form POST http://127.0.0.1:8000/simple_snippets/ code="print(123)"
            http --json POST http://127.0.0.1:8000/simple_snippets/ code="print(456)"
        """
        code = "hello world"
        snippet = SimpleSnippet.objects.create(code=code)

        address = shortcuts.reverse("simple_snippet_list")
        response = self.client.get(address)
        self.assertEquals(response.status_code, 200)
        correct_response_data = [{'id': 1, 'code': 'hello world'}]
        self.assertEquals(response.data, correct_response_data)

        snippet.delete()

    def test_json_snippet_detail(self):
        """
            http http://127.0.0.1:8000/simple_snippets/1/
        """
        code = "hello world"
        snippet = SimpleSnippet.objects.create(code=code)

        address = shortcuts.reverse("simple_snippet_detail", kwargs={"pk": 1})
        response = self.client.get(address)
        correct_response_data = {'id': 1, 'code': 'hello world'}
        self.assertEquals(response.data, correct_response_data)

        snippet.delete()

    def test_highlighted(self):
        """
        http http://127.0.0.1:8000/simple_snippets/1/highlighted
        """
        code = "hello world"
        snippet = SimpleSnippet.objects.create(code=code)

        address = shortcuts.reverse("simple_highlighted", args=(1, ))
        response = self.client.get(address)
        self.assertContains(response, text="red")

        snippet.delete()

"""
    http -a admin:password123 POST http://127.0.0.1:8000/snippets/ code="print(789)"
"""

