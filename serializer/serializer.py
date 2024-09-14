"""Serializer researching"""
import io
import django_setting_setup

from datetime import datetime
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer


class Comment:
    """Simple comment"""
    def __init__(self, email, content, created=None):
        self.email = email
        self.content = content
        self.created = created or datetime.now()


class CommentSerializer(serializers.Serializer):
    """Serializer for simple comment"""
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()


def main():
    """test serializer"""
    comment = Comment(email='leila@example.com', content='foo bar')
    serializer = CommentSerializer(comment)
    print(f"serializer_data - {serializer.data}")
    # Serialization
    json_b_string = JSONRenderer().render(serializer.data)
    print(f"json byte string - {json_b_string}")
    # Deserialization
    stream = io.BytesIO(json_b_string)
    json_data_from_b_str = JSONParser().parse(stream)
    print(f"data from b string - {json_data_from_b_str}")


if __name__ == '__main__':
    main()
