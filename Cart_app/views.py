# cart/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages 
from Menu_app.models import Dish
from .cart import Cart
from Menu_app.models import Order, OrderItem

@require_POST
def cart_add(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    cart.add(dish=dish, quantity=1)
    
    messages.success(request, 'Товар додано', extra_tags='item_added')
    

    return redirect(request.META.get('HTTP_REFERER', '/'))

def cart_remove(request, dish_id):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    cart.remove(dish)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

def cart_update(request, dish_id, action):
    cart = Cart(request)
    dish = get_object_or_404(Dish, id=dish_id)
    
    # Отримуємо поточну кількість товару в кошику
    current_quantity = cart.cart.get(str(dish.id), {}).get('quantity', 0)

    if action == 'increment':
        cart.add(dish, quantity=1)
    elif action == 'decrement':
        # Віднімаємо, тільки якщо товару 2 або більше
        if current_quantity > 1:
            cart.add(dish, quantity=-1)
            
    return redirect('cart:cart_detail')

def order_create(request):
    cart = Cart(request)
    
    if not cart.cart:
        return redirect('menu_list') 

    order = Order.objects.create(total_price=cart.get_total_price())
    
    for item in cart:
        dish = item['product']
        quantity = item['quantity']
        
        OrderItem.objects.create(
            order=order,
            dish=dish,
            price=item['price'],
            quantity=quantity
        )
        
        dish.orders_count += quantity
        dish.save()

    cart.clear()
    
    return render(request, 'cart/created.html', {'order': order})