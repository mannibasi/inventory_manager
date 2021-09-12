from inventory import *
import pytest


def test_buy_and_sell_nikes_adidas():
    inventory = Inventory()
    assert inventory.limit == 100
    assert inventory.total_items == 0

    inventory.add_new_stock('Nike Sneakers', 50.00, 10)
    assert inventory.total_items == 10

    inventory.add_new_stock('Adidas Sweatpants', 70.00, 5)
    assert inventory.total_items == 15

    inventory.remove_stock('Nike Sneakers', 2)
    assert inventory.total_items == 13

    inventory.remove_stock('Adidas Sweatpants', 1)
    assert inventory.total_items == 12


def test_default_inventory():
    inventory = Inventory()
    assert inventory.limit == 100
    assert inventory.total_items == 0


def test_custom_inventory_limit():
    inventory = Inventory(limit=25)
    assert inventory.limit == 25
    assert inventory.total_items == 0


@pytest.fixture
def no_stock_inventory():
    return Inventory(10)


@pytest.fixture
def ten_stock_inventory():
    inventory = Inventory(20)
    inventory.add_new_stock('Puma Test', 100.00, 8)
    inventory.add_new_stock('Reebok Test', 25.00, 2)
    return inventory


@pytest.mark.parametrize('name,price,quantity,exception', [
    ('Test Jacket', 10.00, 0, InvalidQuantityException(
        'Cannot add a quantity of 0. All new stocks must have at least 1 item')),
    ('Test Jacket', 10.00, 25, NoSpaceException(
        'Cannot add these 25 items. Only 10 more items can be stored')),
    ('Test Jacket', 10.00, 5, None)
])
def test_add_new_stock(no_stock_inventory, name, price, quantity, exception):
    try:
        no_stock_inventory.add_new_stock(name, price, quantity)
    except (InvalidQuantityException, NoSpaceException) as inst:
        assert isinstance(inst, type(exception))
        assert inst.args == exception.args
    else:
        assert no_stock_inventory.total_items == 5
        assert no_stock_inventory.stocks['Test Jacket']['price'] == 10.00
        assert no_stock_inventory.stocks['Test Jacket']['quantity'] == 5


@pytest.mark.parametrize('name,quantity,exception,new_quantity,new_total', [
    ('Puma Test', 0, InvalidQuantityException(
        'Cannot remove a quantity of 0. Must remove at least 1 item'), 0, 0),
    ('Not Here', 5, ItemNotFoundException(
        'Could not find Not Here in our stocks. Cannot remove non-existing stock'), 0, 0),
    ('Puma Test', 25, InvalidQuantityException(
        'Cannot remove these 25 items. Only 8 items are in stock'), 0, 0),
    ('Puma Test', 5, None, 3, 5)
])
def test_remove_stock(ten_stock_inventory, name, quantity, exception, new_quantity, new_total):
    try:
        ten_inventory.remove_stock(name, quantity)
    except (InvalidQuantityException, NoSpaceException, ItemNotFoundException) as inst:
        assert isinstance(inst, type(exception))
        assert inst.args == exception.args
    else:
        assert ten_stock_inventory.stocks[name]['quantity'] == new_quantity
        assert ten_stock_inventory.total_items == new_total
