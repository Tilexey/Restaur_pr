from django.db import models

# Create your models here.
class Dish(models.Model):
    image = models.ImageField(upload_to='static/', null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    ingredients = models.CharField(max_length=400, null=True, blank=True)
    orders_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    # Тут можна додати ім'я клієнта, телефон і т.д.

    def __str__(self):
        return f"Замовлення №{self.id}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.dish.name}"
    
    

    