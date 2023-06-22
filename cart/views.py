from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from store.models import Product, ProductVariation
from .models import Cart, ItemInCart
from extras.utility import UtilityManager
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
class CartView(View):

    def get(self, request, total=0, quantity=0, *args, **kwargs):
        context = {}
        tax = 0
        grand_total = 0
        the_cart_items = None

        the_utility = UtilityManager(request)

        try:
            if request.user.is_authenticated:
                the_cart_items = ItemInCart.objects.filter(user=request.user, is_active=True)
            else:
                the_cart = Cart.objects.get(cart_id=the_utility.get_or_create_session())
                the_cart_items = ItemInCart.objects.filter(cart=the_cart, is_active=True)
            for cart_item in the_cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass
        
        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': the_cart_items,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'thesite/cart.html', context)

class AddCartView(View):

    def post(self, request, product_id, *args, **kwargs):
        current_user = request.user
        the_product = Product.objects.get(id=product_id)
        the_utility = UtilityManager(request)
        if current_user.is_authenticated:
            product_variations = []

            for key, value in request.POST.items():
                try:
                    the_variation = ProductVariation.objects.get(product=the_product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(the_variation)
                except ProductVariation.DoesNotExist:
                    pass

            is_cart_item_exists = ItemInCart.objects.filter(product=the_product, user=current_user).exists()
            if is_cart_item_exists:
                the_item_cart = ItemInCart.objects.filter(product=the_product, user=current_user)
                existing_variation_list = []
                ids = []
                for item in the_item_cart:
                    existing_variation = item.variations.all()
                    existing_variation_list.append(list(existing_variation))
                    ids.append(item.id)

                if product_variations in existing_variation_list:
                    index = existing_variation_list.index(product_variations)
                    item_id = ids[index]
                    item_in_cart = ItemInCart.objects.get(product=the_product, id=item_id)
                    item_in_cart.quantity += 1
                    item_in_cart.save()
                else: 
                    itemcartobj = ItemInCart.objects.create(product=the_product, quantity = 1, user = current_user, is_active = True)
                    if len(product_variations) > 0:
                        itemcartobj.variations.clear()
                        itemcartobj.variations.add(*product_variations)
                    itemcartobj.save()
            else:
                the_item_cart = ItemInCart()
                the_item_cart.product = the_product
                the_item_cart.user = current_user
                the_item_cart.quantity = 1
                the_item_cart.is_active = True
                the_item_cart.save()
                
                if len(product_variations) > 0:
                    the_item_cart.variations.clear()
                    the_item_cart.variations.add(*product_variations)
                    the_item_cart.save()

            return redirect('cart_view')
        else:
            product_variations = []

            for key, value in request.POST.items():
                try:
                    the_variation = ProductVariation.objects.get(product=the_product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(the_variation)
                except ProductVariation.DoesNotExist:
                    pass

            try:
                the_cart = Cart.objects.get(cart_id=the_utility.get_or_create_session())
                the_cart.save() #if cart is already exists
            except Cart.DoesNotExist:
                the_cart = Cart()
                the_cart.cart_id = the_utility.get_or_create_session()
                the_cart.save()


            is_cart_item_exists = ItemInCart.objects.filter(product=the_product, cart=the_cart).exists()
            if is_cart_item_exists:
                the_item_cart = ItemInCart.objects.filter(product=the_product, cart=the_cart)
                existing_variation_list = []
                ids = []
                for item in the_item_cart:
                    existing_variation = item.variations.all()
                    existing_variation_list.append(list(existing_variation))
                    ids.append(item.id)

                print("existing_variation_list---", existing_variation_list)

                if product_variations in existing_variation_list:
                    index = existing_variation_list.index(product_variations)
                    item_id = ids[index]
                    item_in_cart = ItemInCart.objects.get(product=the_product, id=item_id)
                    item_in_cart.quantity += 1
                    item_in_cart.save()
                else: 
                    itemcartobj = ItemInCart.objects.create(product=the_product, quantity = 1, cart = the_cart, is_active = True)
                    if len(product_variations) > 0:
                        itemcartobj.variations.clear()
                        itemcartobj.variations.add(*product_variations)
                    itemcartobj.save()
            else:
                the_item_cart = ItemInCart()
                the_item_cart.product = the_product
                the_item_cart.cart = the_cart
                the_item_cart.quantity = 1
                the_item_cart.is_active = True
                the_item_cart.save()
                
                if len(product_variations) > 0:
                    the_item_cart.variations.clear()
                    the_item_cart.variations.add(*product_variations)
                    the_item_cart.save()

            return redirect('cart_view')

class RemoveCartView(View):

    def get(self, request, product_id, cart_item_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        try:
            if request.user.is_authenticated:
                the_cart_item = ItemInCart.objects.get(product=product, user=request.user, id=cart_item_id)
            else:
                the_utility = UtilityManager(request)
                the_cart = Cart.objects.get(cart_id=the_utility.get_or_create_session())
                the_cart_item = ItemInCart.objects.get(product=product, cart=the_cart, id=cart_item_id)
            if the_cart_item.quantity > 1:
                the_cart_item.quantity -= 1
                the_cart_item.save()
            else:
                the_cart_item.delete()
        except:
            pass
        return redirect('cart_view')

class RemoveCartItemView(View):

    def get(self, request, product_id, cart_item_id, *args, **kwargs):
        product = get_object_or_404(Product, id=product_id)
        if request.user.is_authenticated:
            the_cart_item = ItemInCart.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            the_utility = UtilityManager(request)
            the_cart = Cart.objects.get(cart_id=the_utility.get_or_create_session())
            the_cart_item = ItemInCart.objects.get(product=product, cart=the_cart, id=cart_item_id)
        
        the_cart_item.delete()
        return redirect('cart_view')


class CheckoutView(View):

    @method_decorator(login_required(login_url='/accounts/login/'))
    def get(self, request, total=0, quantity=0, *args, **kwargs):
        context = {}
        tax = 0
        grand_total = 0
        the_cart_items = None

        the_utility = UtilityManager(request)

        try:
            if request.user.is_authenticated:
                the_cart_items = ItemInCart.objects.filter(user=request.user, is_active=True)
            else:
                the_cart = Cart.objects.get(cart_id=the_utility.get_or_create_session())
                the_cart_items = ItemInCart.objects.filter(cart=the_cart, is_active=True)
            for cart_item in the_cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity
            tax = (2 * total)/100
            grand_total = total + tax
        except ObjectDoesNotExist:
            pass
        
        context = {
            'total': total,
            'quantity': quantity,
            'cart_items': the_cart_items,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'thesite/checkout.html', context)