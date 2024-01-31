from rest_framework import serializers

# from .models import SimpleSnippet


class TrivialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    code = serializers.CharField(style={'base_template': 'textarea.html'})

# class SimpleSnippetSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     code = serializers.CharField(style={'base_template': 'textarea.html'})
#     title = serializers.CharField(required=False, allow_blank=True, max_length=100)
#     linenos = serializers.BooleanField(required=False)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return SimpleSnippet.objects.create(**validated_data)
#
#     def update(self, model_instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         model_instance.title = validated_data.get('title', model_instance.title)
#         model_instance.code = validated_data.get('code', model_instance.code)
#         model_instance.linenos = validated_data.get('linenos', model_instance.linenos)
#         model_instance.language = validated_data.get('language', model_instance.language)
#         model_instance.style = validated_data.get('style', model_instance.style)
#         model_instance.save()
#         return model_instance
