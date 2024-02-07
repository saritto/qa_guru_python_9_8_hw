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
    cart = Cart()
    cart.products = {}
    return cart


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(1000) is True, "На складе нет 1000шт"
        assert product.check_quantity(999) is True, "На складе нет 999шт"
        assert product.check_quantity(1) is True, "На складе нет 1шт"
        assert product.check_quantity(1001) is False, "На складе есть 1001шт"
        pass

    def test_product_buy_success_case(self, product):
        # TODO напишите проверки на метод buy
        initial_quantity = product.quantity
        product.buy(10)
        assert product.quantity == initial_quantity - 10
        pass

    def test_product_buy_zero_case(self, product):
        # TODO напишите проверки на метод buy
        initial_quantity = product.quantity
        product.buy(0)
        assert product.quantity == initial_quantity
        pass

    def test_product_buy_minus_quantity(self, product):
        # TODO напишите проверки на метод buy
        initial_quantity = product.quantity
        try:
            product.buy(-1)
        except ValueError as e:
            assert str(e) == "Не корректное значение"
        assert product.quantity == initial_quantity
        pass

    def test_product_buy_more_than_available(self, product):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        initial_quantity = product.quantity
        try:
            product.buy(1001)
        except ValueError as e:
            assert str(e) == "Не хватает продуктов"
        assert product.quantity == initial_quantity
        pass


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_add_product_empty_cart(self, cart):
        product = Product("book", 100, "This is a book", 1000)
        assert len(cart.products) == 0
        cart.add_product(product, 5)
        assert cart.products[product] == 5
        assert len(cart.products) == 1
        pass

    def test_add_product_not_empty_cart(self, cart):
        product = Product("book", 100, "This is a book", 1000)
        cart.products = {
            product: 5
        }
        assert cart.products[product] == 5
        cart.add_product(product, 15)
        assert cart.products[product] == 20
        assert len(cart.products) == 1
        pass

    def test_remove_product_without_remove_count(self, cart):
        product = Product("book", 100, "This is a book", 1000)
        cart.products = {
            product: 20
        }
        assert cart.products[product] == 20
        cart.remove_product(product)
        assert len(cart.products) == 0
        assert cart.products.get(product, 0) == 0
        pass

    def test_remove_product_bigger_remove_count(self, cart):
        product = Product("book", 100, "This is a book", 1000)
        cart.products = {
            product: 20
        }
        assert cart.products[product] == 20
        cart.remove_product(product, 50)
        assert len(cart.products) == 0
        pass

    def test_remove_product_smaller_remove_count(self, cart):
        product = Product("book", 100, "This is a book", 1000)
        cart.products = {
            product: 20
        }
        assert cart.products[product] == 20
        cart.remove_product(product, 10)
        assert cart.products[product] == 10
        pass

    def test_clear(self, cart):
        product = Product("book", 100, "This is a book", 1000)
        cart.products = {
            product: 20
        }
        assert cart.products[product] == 20
        cart.clear()
        assert len(cart.products) == 0
        pass

    def test_get_total_price(self, cart):
        product = Product("book", 100, "This is a book", 1000)
        product2 = Product("book2", 200, "This is a book2", 1000)
        cart.products = {
            product: 20,
            product2: 5
        }
        assert cart.get_total_price() == 3000
        cart.clear()
        assert cart.get_total_price() == 0
        pass

    def test_buy(self, cart):
        product = Product("book", 100, "This is a book", 1000)
        cart.products = {
            product: 20
        }
        assert cart.products[product] == 20
        cart.buy()
        assert product.quantity == 980  # проверка склада
        assert cart.products[product] == 0  # проверка корзины
        pass

    def test_buy_more_than_have(self, cart):
        product = Product("book", 100, "This is a book", 100)
        cart.products = {
            product: 120
        }
        assert cart.products[product] == 120
        with pytest.raises(ValueError):
            cart.buy()
        assert product.quantity == 100  # проверка склада
        assert cart.products[product] == 120  # проверка корзины
        pass
