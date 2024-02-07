class Product:
    """
    Класс продукта
    """
    name: str
    price: float
    description: str
    quantity: int

    def __init__(self, name, price, description, quantity):
        self.name = name
        self.price = price
        self.description = description
        self.quantity = quantity

    def check_quantity(self, quantity) -> bool:
        """
        TODO Верните True если количество продукта больше или равно запрашиваемому
            и False в обратном случае
        """
        if self.quantity >= quantity >= 0:
            return True
        elif self.quantity < quantity:
            return False
        else:
            raise ValueError("Не корректное значение")

    def buy(self, quantity):
        """
        TODO реализуйте метод покупки
            Проверьте количество продукта используя метод check_quantity
            Если продуктов не хватает, то выбросите исключение ValueError
        """
        if self.check_quantity(quantity):
            print("Продукты в достаточном количестве")
            self.quantity = self.quantity - quantity
        elif not self.check_quantity(quantity):
            raise ValueError("Не хватает продуктов")
        else:
            raise NotImplementedError

    def __hash__(self):
        return hash(self.name + self.description)


class Cart:
    """
    Класс корзины. В нем хранятся продукты, которые пользователь хочет купить.
    TODO реализуйте все методы класса
    """

    # Словарь продуктов и их количество в корзине
    products: dict[Product, int]

    def __init__(self):
        # По-умолчанию корзина пустая
        self.products = {}

    def add_product(self, product: Product, buy_count=1):
        """
        Метод добавления продукта в корзину.
        Если продукт уже есть в корзине, то увеличиваем количество
        """
        if product in self.products:
            self.products[product] += buy_count
        elif product not in self.products:
            self.products[product] = buy_count
        else:
            raise NotImplementedError

    def remove_product(self, product: Product, remove_count=None):
        """
        Метод удаления продукта из корзины.
        Если remove_count не передан, то удаляется вся позиция
        Если remove_count больше, чем количество продуктов в позиции, то удаляется вся позиция
        """
        if product in self.products:
            if remove_count is None or remove_count >= self.products[product]:
                del self.products[product]
            elif remove_count < self.products[product]:
                self.products[product] -= remove_count
            else:
                raise NotImplementedError

    def clear(self):
        self.products = {}

    def get_total_price(self) -> float:
        total_price = 0.0
        for product, quantity in self.products.items():
            total_price += product.price * quantity
        return total_price

    def buy(self):
        """
        Метод покупки.
        Учтите, что товаров может не хватать на складе.
        В этом случае нужно выбросить исключение ValueError
        """
        for product, quantity in self.products.items():
            if not product.check_quantity(self.products[product]):
                raise ValueError("Недостаточно товаров на складе")
            elif product.check_quantity(self.products[product]):
                product.buy(self.products[product])
                self.products[product] = self.products[product] - quantity
            else:
                raise NotImplementedError
