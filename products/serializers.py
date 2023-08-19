from rest_framework import reverse
from rest_framework import serializers

from .models import Category, Product, File
from rest_framework.request import Request


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'description', 'avatar', 'url']


class FileSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='file-detail'
    # )

    url = serializers.SerializerMethodField()
    file_type = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ['id', 'title', 'file', 'file_type', 'url']

    def get_url(self, obj):
        kwargs = {
            'product_id': obj.products.pk,
            'pk': obj.pk,
        }
        url = reverse.reverse('file-detail', kwargs=kwargs)
        # f'/files/{obj.products.pk}/{obj.pk}/'
        return self.context['request'].build_absolute_uri(url)

    def get_file_type(self, obj):
        return obj.get_file_type_display()


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    categories = CategorySerializer(many=True)
    # files = FileSerializer(many=True)

    # foo = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'avatar', 'categories', 'url']

    # def get_foo(self, obj):
    #     return FileSerializer(File.objects.filter(products= obj), many=True).data
