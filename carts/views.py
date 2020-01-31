from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .models import Cart, CartItem
from products.models import Product 
from products.dict_key import dict_key
# Create your views here.

def viewCart(request):
    cart = None
    try:
        the_id = request.session['cart_id']
    except:
        the_id = None
    if the_id:                
        cart = Cart.objects.get(id=the_id)
        amount = cart.total
        if(amount==0):
            massege = "Your cart is empty"
            context = {'cart':cart, 'empty': massege}         
            template = "cart/view.html"
            return render(request, template, context)

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
        print(discount)        
        context = {'cart':cart,
                    'discount': discount}
    else:
        massege = "Your cart is empty"
        context = {'cart':cart, 'empty': massege}
             
    template = "cart/view.html"
    return render(request, template, context)



def update_cart(request, slug):
    request.session.set_expiry(120000)
    try:
        qty = request.GET.get('qty')
        update_qty = True
    except:
        qty = None
        update_qty = False

    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        the_id = new_cart.id
        cart = Cart.objects.get(id=the_id)

    try:
        product = Product.objects.get(slug=slug)
    except Product.DoesNotExist:
        pass
    except:
        pass

    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if created:
        print ("yeah")

    if update_qty and qty:
        if int(qty) == 0:
            cart_item.delete()
        elif int(qty) == -1:
            cart_item.quantity = cart_item.quantity-1
            cart_item.save()    
        elif int(qty) == +1:
            cart_item.quantity = cart_item.quantity+1
            cart_item.save()    
        else:
            cart_item.quantity = qty
            cart_item.save()
    else:
        pass
    # if not cart_item in cart.items.all():
    #     cart.items.add(cart_item)
    # else:
    #     cart.items.remove(cart_item)

    new_total = 0.00
    for item in cart.cartitem_set.all():
        line_total = float(item.product.price)*item.quantity
        item.line_total = line_total
        item.save()
        new_total = new_total+ line_total

    request.session['item_count'] = cart.cartitem_set.count()
    cart.total = float(new_total)
    cart.save() 
    return HttpResponseRedirect(reverse("viewCart"))               


    