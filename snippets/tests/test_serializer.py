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


class SimpleCommentSerializer(serializers.Serializer):
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

    correct_data = {
        'email': 'leila@example.com',
        'content': 'foo bar',
        'created': '2024-01-21T17:26:01.146216Z',
    }

    correct_json_data = '{"email":"leila@example.com","content":"foo bar","created":"2024-01-21T17:26:01.146216Z"}'

    correct_class_data = Comment(email=correct_data['email'],
                                 content=correct_data['content'],
                                 created=datetime.strptime(correct_data['created'], "%Y-%m-%dT%H:%M:%S.%fZ")
                                 )

    queryset_for_correct_data = models.ModelComment.objects.filter(content=correct_data["content"])

    def test_data(self):
        json_data = json.loads(self.correct_json_data)
        assert json_data == self.correct_data

    def test_serializer_for_data(self):
        serializer = SimpleCommentSerializer(data=self.correct_data)
        assert serializer.is_valid()

        self.assertFalse(self.queryset_for_correct_data.exists())
        serializer.save()
        self.assertTrue(self.queryset_for_correct_data.exists())
        self.queryset_for_correct_data.delete()

        byte_json_validated_data = JSONRenderer().render(serializer.validated_data)
        self.assertEquals(byte_json_validated_data, self.correct_json_data.encode())
        json_validated_data_stream = io.BytesIO(byte_json_validated_data)
        stream_data = JSONParser().parse(json_validated_data_stream)
        self.assertEquals(stream_data, self.correct_data)

    def test_serializer_for_json_bytes(self):
        byte_correct_json_data = str.encode(self.correct_json_data)
        json_validated_data_stream = io.BytesIO(byte_correct_json_data)
        data = JSONParser().parse(json_validated_data_stream)
        serializer = SimpleCommentSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        self.assertFalse(self.queryset_for_correct_data.exists())
        serializer.save()
        self.assertTrue(self.queryset_for_correct_data.exists())
        self.queryset_for_correct_data.delete()

        byte_json_validated_data = JSONRenderer().render(serializer.validated_data)
        self.assertEquals(byte_json_validated_data, self.correct_json_data.encode())
        json_validated_data_stream = io.BytesIO(byte_json_validated_data)
        stream_data = JSONParser().parse(json_validated_data_stream)
        self.assertEquals(stream_data, self.correct_data)

    def test_serializer_for_class(self):
        serializer = SimpleCommentSerializer(self.correct_class_data)
        self.assertEquals(self.correct_data, serializer.data)

        byte_json_data = JSONRenderer().render(serializer.data)
        self.assertEquals(byte_json_data, self.correct_json_data.encode())

        json_validated_data_stream = io.BytesIO(byte_json_data)
        stream_data = JSONParser().parse(json_validated_data_stream)
        self.assertEquals(stream_data, self.correct_data)

    def test_serializer_for_model_class(self):
        serializer = CommentModelSerializer(self.correct_class_data)
        self.assertEquals(self.correct_data, serializer.data)

        byte_json_data = JSONRenderer().render(serializer.data)
        self.assertEquals(byte_json_data, self.correct_json_data.encode())

        json_validated_data_stream = io.BytesIO(byte_json_data)
        stream_data = JSONParser().parse(json_validated_data_stream)
        self.assertEquals(stream_data, self.correct_data)

    def test_serializer_for_incorrect_data(self):
        incorrect_data = copy.deepcopy(self.correct_data).update({"unexpected_key": "hello"})
        serializer = SimpleCommentSerializer(data=incorrect_data)
        self.assertFalse(serializer.is_valid())
        assert not serializer.is_valid()

        incorrect_data = copy.deepcopy(self.correct_data).pop("content")
        serializer = SimpleCommentSerializer(data=incorrect_data)
        self.assertFalse(serializer.is_valid())

        incorrect_comment_class_instance = IncorrectComment()
        serializer = SimpleCommentSerializer(incorrect_comment_class_instance)
        with self.assertRaises(AttributeError):
            _ = serializer.data
