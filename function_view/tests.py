from django import shortcuts
from django.test import TestCase, Client
from snippets.models import SimpleSnippet


class DRFStyleFunctionView(TestCase):
    client = Client()

    def test_json_snippet_list(self):

        code = "hello world"
        snippet = SimpleSnippet.objects.create(code=code)

        address = shortcuts.reverse("snippet_list")
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

        address = shortcuts.reverse("function_view:snippet_detail", kwargs={"pk": 1})
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

        address = shortcuts.reverse("simple_highlighted", args=(1,))
        response = self.client.get(address)
        self.assertContains(response, text="red")

        snippet.delete()

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
