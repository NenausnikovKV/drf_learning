import copy
import io
from django import shortcuts
from django.test import TestCase, Client
from rest_framework.parsers import JSONParser

from .models import CodeSnippet


class DjangoStyleViewFunctionTest(TestCase):
    client = Client()
    data = {
        "id": 1,
        "name": "addition",
        "code": "f = 7+9",
        "is_correct": True,
    }

    @property
    def full_data(self):
        """
            Return data dict with id key if id key has not existed.
        """
        try:
            return dict(id=1, **self.data)
        except TypeError:
            # Raise TypeError if key id already exists
            return self.data

    @classmethod
    def setUpTestData(cls):
        CodeSnippet.objects.create(**cls.data)

    @classmethod
    def tearDown(cls):
        CodeSnippet.objects.all().delete()

    def test_json_response(self):
        """
            http http://127.0.0.1:8000/json/
        """
        address = shortcuts.reverse("json_snippets:json_response")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        data = JSONParser().parse(content_reader)
        correct_data = {"greeting": "hi"}
        self.assertIn("greeting", data)
        self.assertEquals(data, correct_data)

    def test_json_snippet_list(self):
        """
            http http://127.0.0.1:8000/json/snippets/
        """
        address = shortcuts.reverse("json_snippets:snippet_list")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        data = JSONParser().parse(content_reader)
        self.assertEquals(data, [self.full_data])

    def test_json_snippet_detail(self):
        """
            http http://127.0.0.1:8000/json/snippets/1
        """

        address = shortcuts.reverse("json_snippets:snippet_detail", kwargs={"pk": 1})
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        data = JSONParser().parse(content_reader)
        self.assertIn("code", data)
        self.assertEquals(data, self.full_data)

"""
    http -a admin:password123 POST http://127.0.0.1:8000/snippets/ code="print(789)"
"""

"""
    http http://127.0.0.1:8000/simple_snippets/

    http http://127.0.0.1:8000/simple_snippets/ Accept:application/json
    http http://127.0.0.1:8000/simple_snippets.json


    http http://127.0.0.1:8000/simple_snippets/ Accept:text/html
    http http://127.0.0.1:8000/simple_snippets.api

    http --form POST http://127.0.0.1:8000/simple_snippets/ code="print(123)"
    http --json POST http://127.0.0.1:8000/simple_snippets/ code="print(456)"
"""

"""
    http -a admin:password123 POST http://127.0.0.1:8000/snippets/ code="print(789)"
"""
"""

    http http://127.0.0.1:8000/simple_snippets/

    http http://127.0.0.1:8000/simple_snippets/ Accept:application/json
    http http://127.0.0.1:8000/simple_snippets.json


    http http://127.0.0.1:8000/simple_snippets/ Accept:text/html
    http http://127.0.0.1:8000/simple_snippets.api

    http --form POST http://127.0.0.1:8000/simple_snippets/ code="print(123)"
    http --json POST http://127.0.0.1:8000/simple_snippets/ code="print(456)"
"""
