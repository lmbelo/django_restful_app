from rest_framework import serializers
from shopping_list.models import ShoppingItem, ShoppingList

class ShoppingItemSerializer(serializers.ModelSerializer):

    class Meta:

        model = ShoppingItem
        fields = ["id", "name", "purchased"]
        read_only_fields = ("id",)


    def create(self, validated_data, **kwargs):

        validated_data['shopping_list_id'] = self.context['request'].parser_context['kwargs']['pk']
        return super(ShoppingItemSerializer, self).create(validated_data)


class ShoppingListSerializer(serializers.ModelSerializer):

    shopping_items = ShoppingItemSerializer(many=True, read_only=True)


    class Meta:

        model = ShoppingList
        fields = ['id', 'name', 'shopping_items']