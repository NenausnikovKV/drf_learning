import io
from datetime import datetime
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from django.test import TestCase
import json
from snippets import models


# ------ class -------------------------------------------------------------------------------------------------------

class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


# ------ serializer ---------------------------------------------------------------------------------------------------


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


# ------ model serializer ---------------------------------------------------------------------------------------------


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModelComment
        fields = ["email"]


# ------ serializer test ----------------------------------------------------------------------------------------------


class SerializerCreatingTest(TestCase):

    dict_comment = {
        'email': 'leila@example.com',
        'content': 'foo bar',
        'created': '2024-01-21T17:26:01.146216Z',
    }

    json_comment = '{"email":"leila@example.com","content":"foo bar","created":"2024-01-21T17:26:01.146216Z"}'

    comment = Comment(email='leila@example.com', content='foo bar')

    def test_data(self):
        json_data = json.loads(self.json_comment)
        assert json_data == self.dict_comment

    def test_creating_serializer_from_data(self):
        serializer = CommentSerializer(data=self.dict_comment)
        serializer.is_valid()
        print(serializer.validated_data)
        content = JSONRenderer().render(serializer.validated_data)
        print(content)

    def test_creating_serializer_from_json_bytes(self):
        byte_str = str.encode(self.json_comment)
        stream = io.BytesIO(byte_str)
        data = JSONParser().parse(stream)
        serializer = CommentSerializer(data=data)
        serializer.is_valid()

    def test_serializer_from_class(self):
        serializer = CommentSerializer(self.comment)
