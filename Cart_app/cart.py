from decimal import Decimal
from django.conf import settings
from Menu_app.models import Dish  # Імпортуємо вашу модель страви

class Cart:
    def __init__(self, request):
        """Ініціалізація кошика"""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            # Зберігаємо порожній кошик у сесії
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, dish, quantity=1, update_quantity=False):
        """Додавання товару в кошик або оновлення кількості"""
        product_id = str(dish.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(dish.price)}
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Позначаємо сесію як "змінену", щоб Django її зберіг
        self.session.modified = True

    def remove(self, dish):
        """Видалення товару"""
        product_id = str(dish.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Перебір товарів у кошику та отримання їх з бази даних"""
        product_ids = self.cart.keys()
        dishes = Dish.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for dish in dishes:
            cart[str(dish.id)]['product'] = dish

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def get_total_price(self):
        """Загальна вартість кошика"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очищення кошика (наприклад, після покупки)"""
        del self.session['cart']
        self.save()