import pytest

from shopping_list.models import ShoppingItem, ShoppingList


@pytest.fixture(scope="session")
def create_shopping_item():
    def _create_shopping_item(name):
        shopping_list = ShoppingList.objects.create(name="My shopping list")
        shopping_item = ShoppingItem.objects.create(name=name, purchased=False, shopping_list=shopping_list)

        return shopping_item

    return _create_shopping_item