from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from carts.models import Cart
from .models import Order
from .utils import id_generator
from django.contrib.auth.decorators import login_required
from products.dict_key import dict_key
# Create your views here.

@login_required
def checkout(request):
    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse('viewCart'))
        
    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order(cart=cart)
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
    except:
        HttpResponseRedirect(reverse('viewCart'))

    if new_order.status == "Finished":
        # cart.delete()
        del request.session['cart_id']
        del request.session['item_count']
    
    discount = {}
    total_price = 0
    total_discount = 0
    cart_items =  cart.cartitem_set.all()
    for i in range(len(cart_items)):
        item = cart_items[i].product.id
        price = cart_items[i].product.price
        total_price = total_price+price
        sale = cart_items[i].product.sale
        less = price - sale
        total_discount = total_discount+less
        if(price > 0):
            discount[item] = int((less/price)*100)
        else:
            discount[item] = 0    
    if(total_price > 0):
        percent_discount = int((total_discount/total_price)*100)
    else:
        percent_discount = 0        
    discount["total_discount"] = percent_discount
    context = {
        'cart': cart,
        'order': new_order,
        'discount': discount}
    template = "order/order.html"
    return render(request, template, context)