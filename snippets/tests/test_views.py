import io

from django import shortcuts
from django.contrib.auth.models import User
from django.db import transaction
from django.test import TestCase, Client
from rest_framework.parsers import JSONParser

from snippets.models import Snippet


class SnippetsTest(TestCase):

    def setUp(self):
        self.client = Client()
        with transaction.atomic():
            self.user = User.objects.create_user(username="kostya", email="kostya@mail.com", password="kostya")

    def tearDown(self):
        Snippet.objects.all().delete()

    def test_root_page(self):
        """
            http http://127.0.0.1:8000/class/
        """
        address = shortcuts.reverse("snippets:root")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        data = JSONParser().parse(content_reader)
        self.assertIn("users", data)
        self.assertIn("snippets", data)

    def test_get_snippet_list(self):
        """
            http http://127.0.0.1:8000/class/snippets/
        """
        big_id = 10264
        data = {
            "id": big_id,
            "code": "separator.join(abses)",
            "owner": self.user,
        }
        with transaction.atomic():
            Snippet.objects.create(**data)

        address = shortcuts.reverse("snippets:snippet-list")
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data[0])
        self.assertIn("code", response_data[0])

    def test_create_snippet(self):
        """
            http -a kostya:kostya  POST http://127.0.0.1:8000/class/snippets/ code="print(456)" name="assd" is_correct=true
        """
        address = shortcuts.reverse("snippets:snippet-list")

        login_success = self.client.login(username="kostya", email="kostya@mail.com", password="kostya")
        self.assertTrue(login_success)
        post_data = {
            "code": "print('hello')",
        }

        response = self.client.post(address, data=post_data, content_type="application/json")
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data)
        self.assertIn("code", response_data)

        response_id = int(response_data["id"])
        get_by_response_id_queryset = Snippet.objects.filter(id=response_id)
        self.assertTrue(get_by_response_id_queryset.exists())
        Snippet.objects.filter(id=response_id).delete()
        self.assertFalse(get_by_response_id_queryset.exists())

        with self.assertRaises(Snippet.DoesNotExist):
            wrong_id = 99999999
            _ = Snippet.objects.get(id=wrong_id)


    def test_get_snippet_detail(self):
        """
            http http://127.0.0.1:8000/class/snippets/10265
        """
        big_id = 10265
        data = {
            "id": big_id,
            "code": "f = 7+9",
            "owner": self.user,
        }
        with transaction.atomic():
            Snippet.objects.create(**data)

        address = shortcuts.reverse("snippets:snippet-detail", kwargs={"pk": big_id})
        response = self.client.get(address)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)
        self.assertIn("code", response_data)
        self.assertIn("id", response_data)
        self.assertIn("owner", response_data)


    def test_put_snippet(self):
        """
            http -a kostya:kostya PUT http://127.0.0.1:8000/class/snippets/ code="print(456)" name="assd" is_correct=true
        """

        login_success = self.client.login(username="kostya", email="kostya@mail.com", password="kostya")
        self.assertTrue(login_success)

        # I choose huge id and hope testDB never creates so big table
        big_id = 10266
        data = {
            "id": big_id,
            "code": "start code",
            "owner": self.user
        }
        with transaction.atomic():
            Snippet.objects.create(**data)

        address = shortcuts.reverse("snippets:snippet-detail", kwargs={"pk": big_id})
        new_code = "new code"
        new_is_correct = True
        put_data = {
            "id": big_id,
            "code": new_code,
        }
        response = self.client.put(address, data=put_data, content_type="application/json")
        self.assertEquals(response.status_code, 200)
        content_reader = io.BytesIO(response.content)
        response_data = JSONParser().parse(content_reader)

        self.assertIn("id", response_data)
        self.assertIn("code", response_data)

        response_id = int(response_data["id"])
        get_by_response_id_queryset = Snippet.objects.filter(id=response_id)
        self.assertTrue(get_by_response_id_queryset.exists())
        self.assertEquals(response_data["code"], new_code)
        Snippet.objects.filter(id=big_id).delete()

    def test_delete_snippet(self):
        """
            http -a kostya:kostya DELETE http://127.0.0.1:8000/class/snippets/10267
        """
        login_success = self.client.login(username="kostya", email="kostya@mail.com", password="kostya")
        self.assertTrue(login_success)
        # I choose huge id and hope testDB never creates so big table
        big_id = 10267
        data = {
            "id": big_id,
            "code": "start code",
            "owner": self.user
        }
        with transaction.atomic():
            Snippet.objects.create(**data)
        big_id_queryset = Snippet.objects.filter(id=big_id)
        self.assertTrue(big_id_queryset.exists())
        address = shortcuts.reverse("snippets:snippet-detail", kwargs={"pk": big_id})
        response = self.client.delete(address)
        self.assertEquals(response.status_code, 204)
        self.assertFalse(big_id_queryset.exists())
        with self.assertRaises(Snippet.DoesNotExist):
            wrong_id = big_id
            _ = Snippet.objects.get(id=wrong_id)


    def test_static_highlight_page(self):
        """
            http  http://127.0.0.1:8000/class/snippets/10268/highlight
        """
        big_id = 10268
        code = "anything code"
        data = {
            "id": big_id,
            "code": code,
            "owner": self.user
        }
        with transaction.atomic():
            Snippet.objects.create(**data)
        big_id_queryset = Snippet.objects.filter(id=big_id)
        self.assertTrue(big_id_queryset.exists())

        address = shortcuts.reverse("snippets:snippet-highlight", kwargs={"pk": big_id})
        response = self.client.get(address)
        self.assertEquals(response.status_code, 200)
