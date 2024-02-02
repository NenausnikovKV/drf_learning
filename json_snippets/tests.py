import io

from django import shortcuts
from django.db import transaction
from django.test import TestCase, Client
from rest_framework.parsers import JSONParser

from .models import CodeSnippet


class JsonSnippetsTest(TestCase):
    client = Client()

    @classmethod
    def setUpTestData(cls):
        pass

    @classmethod
    def tearDown(cls):
        CodeSnippet.objects.all().delete()

    def test_root_page(self):
        """
            http http://127.0.0.1:8000/json/
        """
        address = shortcuts.reverse("json_snippets:root")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        data = JSONParser().parse(content_reader)
        self.assertIn("json_response", data)
        self.assertIn("snippet_list", data)

    def test_json_response(self):
        """
            http http://127.0.0.1:8000/json/json_response/
        """
        address = shortcuts.reverse("json_snippets:json_response")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        data = JSONParser().parse(content_reader)
        correct_data = {"greeting": "hi"}
        self.assertIn("greeting", data)
        self.assertEquals(data, correct_data)

    def test_get_snippet_list(self):
        """
            http http://127.0.0.1:8000/json/snippets/
        """

        big_id = 10264
        data = {
            "id": big_id,
            "name": "addition",
            "code": "f = 7+9",
            "is_correct": True,
        }
        with transaction.atomic():
            CodeSnippet.objects.create(**data)
        address = shortcuts.reverse("json_snippets:snippet_list")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)
        self.assertEquals(response_data, [data])

    def test_create_snippet(self):
        """
            http POST http://127.0.0.1:8000/json/snippets/ code="print(456)" name="assd" is_correct=true
        """
        address = shortcuts.reverse("json_snippets:snippet_list")


        post_data = {
            "name": "output_message",
            "code": "print('hello')",
            "is_correct": True,
        }

        response = self.client.post(address, data=post_data, content_type="application/json")
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data)
        self.assertIn("name", response_data)
        self.assertIn("code", response_data)
        self.assertIn("is_correct", response_data)

        response_id = int(response_data["id"])
        get_by_response_id_queryset = CodeSnippet.objects.filter(id=response_id)
        self.assertTrue(get_by_response_id_queryset.exists())
        CodeSnippet.objects.filter(id=response_id).delete()

        with self.assertRaises(CodeSnippet.DoesNotExist):
            wrong_id = 99999999
            _ = CodeSnippet.objects.get(id=wrong_id)

    def test_get_snippet_detail(self):
        """
            http http://127.0.0.1:8000/json/snippets/1
        """

        big_id = 10265
        data = {
            "id": big_id,
            "name": "addition",
            "code": "f = 7+9",
            "is_correct": True,
        }
        with transaction.atomic():
            CodeSnippet.objects.create(**data)

        address = shortcuts.reverse("json_snippets:snippet_detail", kwargs={"pk": big_id})
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)
        self.assertIn("code", response_data)
        self.assertEquals(response_data, data)

    def test_put_snippet(self):
        """
            http PUT http://127.0.0.1:8000/json/snippets/ code="print(456)" name="assd" is_correct=true
        """

        # I choose huge id and hope testDB never creates so big table
        big_id = 10266
        with transaction.atomic():
            CodeSnippet.objects.create(id=big_id, name="start_name", code="start code", is_correct=False)

        address = shortcuts.reverse("json_snippets:snippet_detail", kwargs={"pk": big_id})
        new_name = "new_name"
        new_code = "new code"
        new_is_correct = True
        put_data = {
            "id": big_id,
            "name": new_name,
            "code": new_code,
            "is_correct": new_is_correct,
        }
        response = self.client.put(address, data=put_data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data)
        self.assertIn("name", response_data)
        self.assertIn("code", response_data)
        self.assertIn("is_correct", response_data)

        response_id = int(response_data["id"])
        get_by_response_id_queryset = CodeSnippet.objects.filter(id=response_id)
        self.assertTrue(get_by_response_id_queryset.exists())
        self.assertEquals(response_data["name"], new_name)
        self.assertEquals(response_data["code"], new_code)
        self.assertEquals(response_data["is_correct"], new_is_correct)
        CodeSnippet.objects.filter(id=big_id).delete()

    def test_delete_snippet(self):
        """
            http DELETE http://127.0.0.1:8000/json/snippets/1
        """
        # I choose huge id and hope testDB never creates so big table
        big_id = 10267
        with transaction.atomic():
            CodeSnippet.objects.create(id=big_id, name="subtraction", code="k=7-9", is_correct=True)
        big_id_queryset = CodeSnippet.objects.filter(id=big_id)
        self.assertTrue(big_id_queryset.exists())
        address = shortcuts.reverse("json_snippets:snippet_detail", kwargs={"pk": big_id})
        response = self.client.delete(address)
        self.assertEquals(response.status_code, 204)
        self.assertFalse(big_id_queryset.exists())
        with self.assertRaises(CodeSnippet.DoesNotExist):
            wrong_id = big_id
            _ = CodeSnippet.objects.get(id=wrong_id)
