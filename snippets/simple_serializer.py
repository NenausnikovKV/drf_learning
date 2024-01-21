import io
from datetime import datetime

from django.db import models
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from snippets.models import ModelComment


class Comment:
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


class SimpleComment:
    def __init__(self, content):
        self.content = content


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelComment
        fields = ["email"]


if __name__ == "__main__":
    comment = Comment(email='leila@example.com', content='foo bar')
    serializer = CommentSerializer(comment)
    json = JSONRenderer().render(serializer.data)
    print(json)

    stream = io.BytesIO(json)
    data = JSONParser().parse(stream)

    serializer = CommentSerializer(data=data)
    serializer.is_valid()

    print(serializer.validated_data)
