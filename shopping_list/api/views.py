from rest_framework import generics
from rest_framework import viewsets
from shopping_list.api.serializers import ShoppingListSerializer, ShoppingItemSerializer
from shopping_list.models import ShoppingList, ShoppingItem

class ListAddShoppingList(generics.ListCreateAPIView):

    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer


class ShoppingListDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer


class AddShoppingItem(generics.CreateAPIView):

    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer


class ShoppingItemDetail(generics.RetrieveUpdateDestroyAPIView):

    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    lookup_url_kwarg = "item_pk"