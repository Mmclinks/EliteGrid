from rest_framework import serializers
from .models import EliteProduct, GridNode, NodeContact


class NodeContactSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели NodeContact.
    """
    class Meta:
        model = NodeContact
        fields = "__all__"


class EliteProductSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели EliteProduct.
    """
    class Meta:
        model = EliteProduct
        fields = "__all__"


class GridNodeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели GridNode.
    Включает связанные данные о контактах, продуктах и поставщике.
    """
    contact = NodeContactSerializer()
    products = EliteProductSerializer(many=True)
    supplier = serializers.StringRelatedField()

    class Meta:
        model = GridNode
        fields = "__all__"
        read_only_fields = ("debt",)

