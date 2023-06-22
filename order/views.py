from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from cart.models import ItemInCart
from extras.email_handler import EmailHandler
from store.models import Product
from .forms import OrderForm
from .models import Order, OrderLine, Payment
import datetime
import json

# Create your views here.
class OrderView(View):

    def generate_order_no(self, order):
        day = int(datetime.date.today().strftime('%d'))
        month = int(datetime.date.today().strftime('%m'))
        year = int(datetime.date.today().strftime('%Y'))
        the_date = datetime.date(year, month, day)
        current_date = the_date.strftime('%Y%m%d')
        order_no = current_date + str(order.id)
        return order_no
    
    def post(self, request, *args, **kwargs):
        total=0
        quantity=0
        tax = 0
        grand_total = 0

        cart_count = ItemInCart.objects.filter(user=request.user).count()
        cart_items = ItemInCart.objects.filter(user=request.user)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax

        if cart_count <= 0:
            return redirect('store')
        
        the_form = OrderForm(request.POST)
        if the_form.is_valid():
            the_order = Order()
            the_order.user = request.user
            the_order.first_name = the_form.cleaned_data['first_name']
            the_order.last_name = the_form.cleaned_data['last_name']
            the_order.phone = the_form.cleaned_data['phone']
            the_order.email = the_form.cleaned_data['email']
            the_order.address_line1 = the_form.cleaned_data['address_line1']
            the_order.address_line2 = the_form.cleaned_data['address_line2']
            the_order.city = the_form.cleaned_data['city']
            the_order.state = the_form.cleaned_data['state']
            the_order.country = the_form.cleaned_data['country']
            the_order.zip_code = the_form.cleaned_data['zip_code']
            the_order.order_note = the_form.cleaned_data['order_note']
            the_order.order_total = grand_total
            the_order.tax = tax
            the_order.ip = request.META.get('REMOTE_ADDR')
            the_order.is_active = True
            the_order.save()

            order_number = self.generate_order_no(the_order)
            the_order.order_number = order_number
            the_order.save()

            return redirect('order_summery', order_number)
        else:
            return redirect('checkout_view')
        
class OrderSummery(View):

    def get(self, request, order_number, *args, **kwargs):
        total=0
        quantity=0
        tax = 0
        grand_total = 0

        order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)
        cart_items = ItemInCart.objects.filter(user=request.user)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        tax = (2 * total)/100
        grand_total = total + tax

        context = {
            'order': order,
            'cart_items': cart_items,
            'total': total,
            'tax': tax,
            'grand_total': grand_total,
        }
        return render(request, 'thesite/payments.html', context)
        

class PaymentView(View):

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        print(f"body==={body}")
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

        # Store transaction details inside Payment model
        payment = Payment(
            user = request.user,
            payment_id = body['transID'],
            payment_method = body['payment_method'],
            amount_paid = order.order_total,
            status = body['status'],
        )
        payment.save()
        
        order.payment = payment
        order.is_ordered = True
        order.save()

        # Move the cart items to Order Product table
        cart_items = ItemInCart.objects.filter(user=request.user)

        for item in cart_items:
            orderproduct = OrderLine()
            orderproduct.order = order
            orderproduct.payment = payment
            orderproduct.user = request.user
            orderproduct.product = item.product
            orderproduct.quantity = item.quantity
            orderproduct.product_price = item.product.price
            orderproduct.ordered = True
            orderproduct.save()

            cart_item = ItemInCart.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderLine.objects.get(id=orderproduct.id)
            orderproduct.variation.set(product_variation)
            orderproduct.save()

            # Reduce the quantity of the sold products
            product = Product.objects.get(id=item.product_id)
            product.stock -= item.quantity
            product.save()
        
        # Clear cart
        ItemInCart.objects.filter(user=request.user).delete()

        # Send order recieved email to customer
        email_handler = EmailHandler()
        email_handler.send_order_recieved_mail(request.user, request.user.email, order)
        email_handler.send_email()

        res = {
            'order_number': order.order_number,
            'transID': payment.payment_id,
        }
        return JsonResponse(res)

class OrderCompleteView(View):

    def get(self, request, *args, **kwargs):
        payment = None

        order_number = request.GET.get('order_number')
        transID = request.GET.get('payment_id')

        try:
            order = Order.objects.get(order_number=order_number, is_ordered=True)
            ordered_products = OrderLine.objects.filter(order_id=order.id)

            subtotal = 0
            for i in ordered_products:
                subtotal += i.product_price * i.quantity

            if transID:
                payment = Payment.objects.get(payment_id=transID)

            context = {
                'order': order,
                'ordered_products': ordered_products,
                'order_number': order.order_number,
                'transID': transID,
                'payment': payment,
                'subtotal': subtotal,
            }
            return render(request, 'thesite/order_complete.html', context)
        except (Payment.DoesNotExist, Order.DoesNotExist):
            return redirect('site-index-view')