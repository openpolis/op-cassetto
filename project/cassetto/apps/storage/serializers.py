from django.conf import settings
from django.forms import widgets
from rest_framework import serializers
from cassetto.apps.storage.models import Storage, Resource


class StorageSerializer(serializers.ModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='storage-detail')
    code = serializers.SlugField(max_length=settings.CASSETTO.get('STORAGE_NAME_MAX_LENGTH'))
    description = serializers.CharField(widget=widgets.Textarea,
                                        max_length=100000)

    resources = serializers.HyperlinkedRelatedField(view_name='resource-detail', many=True)
    owner = serializers.Field(source='owner.username')

    class Meta:
        model = Storage
        fields = ('url', 'code', 'description', 'owner', 'created_at', 'updated_at')


class StorageDetailSerializer(StorageSerializer):

    resources = serializers.HyperlinkedRelatedField(view_name='resource-detail', many=True)

    class Meta(StorageSerializer.Meta):
        fields = StorageSerializer.Meta.fields +  ('resources', )


class HyperlinkedFileField(serializers.FileField):
    """
    Build a downloadable url for a file of a resource.
    """
    def to_native(self, value):
        return self.context.get('request').build_absolute_uri(value.url)


class ResourceSerializer(serializers.ModelSerializer):

    storage = serializers.HyperlinkedRelatedField(view_name='storage-detail')
    owner = serializers.Field(source='owner.username')
    file_url = HyperlinkedFileField(source='file')

    class Meta:
        model = Resource
        fields = ('name', 'path', 'description', 'file_url', 'owner', 'storage', 'created_at', 'updated_at')
