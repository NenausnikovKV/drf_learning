import copy
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


class IncorrectComment:
    def __init__(self):
        self.any_name = 158

# ------ serializer ---------------------------------------------------------------------------------------------------


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        email = validated_data.get('email')
        content = validated_data.get('content')
        created = validated_data.get('created')
        return models.ModelComment.objects.create(email=email, content=content, created=created)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.content = validated_data.get('content', instance.content)
        instance.created = validated_data.get('created', instance.created)
        instance.save()
        return instance


# ------ model serializer ---------------------------------------------------------------------------------------------


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ModelComment
        fields = ["email", "content", "created"]


# ------ serializer test ----------------------------------------------------------------------------------------------


class SerializerCreatingTest(TestCase):

    dict_comment = {
        'email': 'leila@example.com',
        'content': 'foo bar',
        'created': '2024-01-21T17:26:01.146216Z',
    }

    json_comment = '{"email":"leila@example.com","content":"foo bar","created":"2024-01-21T17:26:01.146216Z"}'

    comment = Comment(email=dict_comment['email'],
                      content=dict_comment['content'],
                      created=datetime.strptime(dict_comment['created'], "%Y-%m-%dT%H:%M:%S.%fZ")
                      )

    test_queryset = models.ModelComment.objects.filter(content=dict_comment["content"])

    def test_data(self):
        json_data = json.loads(self.json_comment)
        assert json_data == self.dict_comment

    def test_serializer_for_data(self):
        serializer = CommentSerializer(data=self.dict_comment)
        assert serializer.is_valid()
        assert self.test_queryset.count() == 0
        serializer.save()
        assert self.test_queryset.count() == 1
        self.test_queryset.delete()
        assert self.test_queryset.count() == 0

        content = JSONRenderer().render(serializer.validated_data)
        assert content == self.json_comment.encode()

        stream = io.BytesIO(content)
        stream_data = JSONParser().parse(stream)
        assert stream_data == self.dict_comment

    def test_serializer_for_class(self):
        serializer = CommentSerializer(self.comment)
        assert self.dict_comment == serializer.data

        content = JSONRenderer().render(serializer.data)
        assert content == self.json_comment.encode()

        stream = io.BytesIO(content)
        stream_data = JSONParser().parse(stream)
        assert stream_data == self.dict_comment

    def test_serializer_for_model_class(self):
        serializer = CommentModelSerializer(self.comment)
        assert self.dict_comment == serializer.data

        content = JSONRenderer().render(serializer.data)
        assert content == self.json_comment.encode()

        stream = io.BytesIO(content)
        stream_data = JSONParser().parse(stream)
        assert stream_data == self.dict_comment

    def test_serializer_for_json_bytes(self):
        byte_str = str.encode(self.json_comment)
        stream = io.BytesIO(byte_str)
        data = JSONParser().parse(stream)
        serializer = CommentSerializer(data=data)
        serializer.is_valid()
        assert self.test_queryset.count() == 0
        serializer.save()
        assert self.test_queryset.count() == 1
        self.test_queryset.delete()
        assert self.test_queryset.count() == 0

        content = JSONRenderer().render(serializer.validated_data)
        assert content == self.json_comment.encode()
        stream = io.BytesIO(content)
        stream_data = JSONParser().parse(stream)
        assert stream_data == self.dict_comment

    def test_serializer_for_incorrect_data(self):
        incorrect_data = copy.deepcopy(self.dict_comment).update({"unexpected key": "hello"})
        serializer = CommentSerializer(data=incorrect_data)
        assert not serializer.is_valid()

        incorrect_data = copy.deepcopy(self.dict_comment).pop("content")
        serializer = CommentSerializer(data=incorrect_data)
        assert not serializer.is_valid()

        incorrect_comment = IncorrectComment()
        serializer = CommentSerializer(incorrect_comment)
        with self.assertRaises(AttributeError):
            _ = serializer.data
