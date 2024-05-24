"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from homework.models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def cart():
    return Cart()


@pytest.fixture
def product2():
    return Product("mouse", 10, "This is a mouse", 20)


@pytest.fixture
def not_empty_cart(product, product2):
    return Cart().add_product(product, 2).add_product(product2, 3)


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1000) is True
        assert product.check_quantity(999) is True
        assert product.check_quantity(1001) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy

        expected = product.quantity - 1
        product.buy(1)

        assert product.quantity == expected

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            assert product.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_products(self, cart, product, product2):
        cart.add_product(product).add_product(product2, 2)

        assert product in cart.products
        assert cart.products[product] == 1
        assert product2 in cart.products
        assert cart.products[product2] == 2

    def test_add_same_product(self, cart, product):
        cart.add_product(product).add_product(product, 2)
        assert cart.products[product] == 3

    def test_remove_products(self, not_empty_cart, product, product2):
        not_empty_cart.remove_product(product, 1).remove_product(product2)
        assert not_empty_cart.products[product] == 1
        assert product2 not in not_empty_cart.products

    def test_remove_non_existent_product(self, cart, product2):
        with pytest.raises(KeyError):
            assert cart.remove_product(product2,3)

    def test_clear(self,not_empty_cart):
        not_empty_cart.clear()
        assert not not_empty_cart.products

    def test_total_price(self, not_empty_cart):
        assert not_empty_cart.get_total_price() == 230

    def test_total_empty_price(self, cart):
        assert cart.get_total_price() == 0

    def test_buy_all(self, not_empty_cart, product, product2):
        not_empty_cart.buy()
        assert product.quantity == 998
        assert product2.quantity == 17
        assert not not_empty_cart.products

    def test_buy_with_not_enough_goods(self, cart, product):
        with pytest.raises(ValueError):
            assert cart.add_product(product, 100000).buy()
