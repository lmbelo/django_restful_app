from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from shopping_list.api.serializers import (
    ShoppingItemSerializer, 
    ShoppingListSerializer, 
    AddMemberSerializer,
    RemoveMemberSerializer)
from shopping_list.models import (
    ShoppingList, 
    ShoppingItem)
from shopping_list.api.permissions import (
    AllShoppingItemsShoppingListMembersOnly,
    ShoppingItemShoppingListMembersOnly,
    ShoppingListMembersOnly,
)
from shopping_list.api.pagination import LargerResultsSetPagination


class ListAddShoppingList(generics.ListCreateAPIView):

    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer

    def perform_create(self, serializer):

        shopping_list = serializer.save()
        shopping_list.members.add(self.request.user)
        return shopping_list
    
    def get_queryset(self):
        return ShoppingList.objects.filter(members=self.request.user).order_by("-last_interaction")
    

class ShoppingListDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
    permission_classes = [ShoppingListMembersOnly]


class AddShoppingItem(generics.CreateAPIView):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    permission_classes = [AllShoppingItemsShoppingListMembersOnly]


class ShoppingItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShoppingItem.objects.all()
    serializer_class = ShoppingItemSerializer
    permission_classes = [ShoppingItemShoppingListMembersOnly]
    lookup_url_kwarg = "item_pk"


class ListAddShoppingItem(generics.ListCreateAPIView):
    serializer_class = ShoppingItemSerializer
    permission_classes = [AllShoppingItemsShoppingListMembersOnly]
    pagination_class = LargerResultsSetPagination
    filter_backends = (filters.OrderingFilter,)
    ordering_fields = ["name", "purchased"]

    def get_queryset(self):
        shopping_list = self.kwargs["pk"]
        queryset = ShoppingItem.objects.filter(shopping_list=shopping_list).order_by("purchased")

        return queryset
    

class ShoppingListAddMembers(APIView):
    permission_classes = [ShoppingListMembersOnly]

    def put(self, request, pk, format=None):
        shopping_list = ShoppingList.objects.get(pk=pk)
        serializer = AddMemberSerializer(shopping_list, data=request.data)
        self.check_object_permissions(request, shopping_list)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ShoppingListRemoveMembers(APIView):
    permission_classes = [ShoppingListMembersOnly]

    def put(self, request, pk, format=None):
        shopping_list = ShoppingList.objects.get(pk=pk)
        serializer = RemoveMemberSerializer(shopping_list, data=request.data)
        self.check_object_permissions(request, shopping_list)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SearchShoppingItems(generics.ListAPIView):
    serializer_class = ShoppingItemSerializer
    search_fields = ["name"]
    filter_backends = (filters.SearchFilter,)

    def get_queryset(self):
        users_shopping_lists = ShoppingList.objects.filter(members=self.request.user)
        queryset = ShoppingItem.objects.filter(shopping_list__in=users_shopping_lists)

        return queryset