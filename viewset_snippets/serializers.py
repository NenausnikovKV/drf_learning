from django.contrib.auth.models import User
from rest_framework import serializers
from viewset_snippets.models import ViewSetSnippet


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # view_name = "snippets:snippet-detail"
    url = serializers.HyperlinkedIdentityField(view_name="snippets:snippet-detail")
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippets:snippet-highlight', format='html')

    class Meta:
        model = ViewSetSnippet
        fields = ['url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="snippets:user-detail")
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippets:snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']
