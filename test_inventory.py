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


def test_add_new_stock_success(no_stock_inventory):
    no_stock_inventory.add_new_stock('Test Jacket', 10.00, 5)
    assert no_stock_inventory.total_items == 5
    assert no_stock_inventory.stocks['Test Jacket']['price'] == 10.00
    assert no_stock_inventory.stocks['Test Jacket']['quantity'] == 5