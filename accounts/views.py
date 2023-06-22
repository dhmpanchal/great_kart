from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from cart.models import Cart, ItemInCart

from extras.utility import UtilityManager
from order.models import Order, OrderLine

from .forms import RegistrationForm, UserForm, UserProfileForm
from .account_handler import AccountHandler
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import Account, UserProfile
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from extras.tokens import account_activation_token
from django.utils.decorators import method_decorator
from extras.email_handler import EmailHandler

import requests


# Create your views here.
class SignUpVire(View):

  def get(self, request, *args, **kwargs):
    context = {}
    form = RegistrationForm()

    context = {
      'form': form,
    }
    return render(request, 'accounts/signup.html', context)

  def post(self, request, *args, **kwargs):
    form = RegistrationForm(request.POST)
    the_handler = AccountHandler()
    current_site = get_current_site(request)
    created = the_handler.create_account(current_site, form=form)
    if created:
      messages.success(request, 'Account created successfully, please check your email address and activate your account!')
      return redirect('register_view')
    else:
      context = {
        'form': form,
      }
      return render(request, 'accounts/signup.html', context)

class LoginVire(View):

    def get(self, request, *args, **kwargs):
      return render(request, 'accounts/login.html')

    def post(self, request, *args, **kwargs):
      email = request.POST.get('email', '')

      user = Account.objects.filter(email=email).first()

      if user is not None:
        if user.is_active and not user.is_admin:
          try:
            the_utility = UtilityManager(request)
            the_cart = Cart.objects.get(cart_id=the_utility.get_or_create_session())
            is_cart_item_exists = ItemInCart.objects.filter(cart=the_cart).exists()
            
            if is_cart_item_exists:
              product_variations = []
              cartitems = ItemInCart.objects.filter(cart=the_cart)
              for ci in cartitems:
                variations = ci.variations.all()
                product_variations.append(list(variations))
              
              the_item_cart = ItemInCart.objects.filter(user=user)
              existing_variation_list = []
              ids = []
              for item in the_item_cart:
                  existing_variation = item.variations.all()
                  existing_variation_list.append(list(existing_variation))
                  ids.append(item.id)

              for pr in product_variations:
                if pr in existing_variation_list:
                  index = existing_variation_list.index(pr)
                  item_id = ids[index]
                  item_in_cart = ItemInCart.objects.get(id=item_id)
                  item_in_cart.quantity += 1
                  item_in_cart.user = user
                  item_in_cart.save()
                else:
                  item_in_cart = ItemInCart.objects.filter(cart=the_cart)
                  for item in item_in_cart:
                    item.user = user
                    item.save()

          except Cart.DoesNotExist:
            pass

          login(request, user)
          messages.success(request, 'Login successful!')
          try:
            url  = request.META['HTTP_REFERER']
            query = requests.utils.urlparse(url).query
            params = dict(x.split('=') for x in query.split('&'))

            if 'next' in params:
              next_page = params['next']
              return redirect(next_page)
          except:
            return redirect('dashboard')
        else:
          messages.error(request, 'User is not active')
          return redirect('login_view')
      else:
        messages.error(request, 'User credentials are not valid')
        return redirect('login_view')

@login_required(login_url='/accounts/login/')
def logout_view(request):
  logout(request)
  messages.success(request, 'You are now logged out!')
  return redirect('login_view')


class AccountActivationView(View):

  def get(self, request, uidb64, token, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect(reverse_lazy('dashboard'))
    else:
        return HttpResponse('Activation link is invalid or your account is already Verified! Try To Login')


class DashboardView(View):
  @method_decorator(login_required(login_url='/accounts/login/'))
  def get(self, request, *args, **kwargs):
    orders = Order.objects.order_by('-created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()

    userprofile = UserProfile.objects.get(user_id=request.user.id)
    context = {
        'orders_count': orders_count,
        'userprofile': userprofile,
    }
    return render(request, 'thesite/dashboard.html', context)


class ForgotPAsswordView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'accounts/forgotpassword.html')
  
  def post(self, request, *args, **kwargs):
    email = request.POST.get('email')
    user_exists = Account.objects.filter(email__exact=email).exists()

    if user_exists:
      try:
        user = Account.objects.get(email__exact=email)
        email_handler  = EmailHandler()
        email_handler.send_forgot_password_mail(get_current_site(request), user, email)
        email_handler.send_email()
        messages.success(request, 'Please check your mail, we have sent reset password link to your email!')
        return redirect(reverse_lazy('forgotpassword'))
      except (Account.DoesNotExist) as e:
        print(f"Error getting user:: {e}")
        messages.error(request, 'Account does not exist!')
        return redirect(reverse_lazy('forgotpassword'))
    else:
      messages.error(request, 'Account does not exist!')
      return redirect(reverse_lazy('forgotpassword'))

class ResetPasswordConfirmView(View):

  def get(self, request, uidb64, token, *args, **kwargs):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist) as e:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        request.session['uid'] = uid
        return redirect('password_change')
    else:
        messages.error(request, 'Your Link has been expired!')
        return redirect('login_view')
    
class ChangePAsswordView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'accounts/chencge_password.html')
  
  def post(self, request, *args, **kwargs):
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    uid = request.session.get('uid')

    try:
      user = Account.objects.get(pk=uid)
    except Account.DoesNotExist as e:
      messages.error(request, 'User not exist!')
      return redirect(reverse_lazy('password_change'))
    
    if password == confirm_password:
      user.set_password(password)
      user.save()
      messages.success(request, 'Password changed successfully!')
      return redirect('login_view')
    else:
      messages.error(request, 'Password does not match!')
      return redirect(reverse_lazy('password_change'))

class MyOrderView(View):
  @method_decorator(login_required(login_url='/accounts/login/'))
  def get(self, request, *args, **kwargs):
    orders = Order.objects.filter(user=request.user, is_ordered=True).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'thesite/myorder.html', context)

class ProfileView(View):
  @method_decorator(login_required(login_url='/accounts/login/'))
  def get(self, request, *args, **kwargs):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    user_form = UserForm(instance=request.user)
    profile_form = UserProfileForm(instance=userprofile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'userprofile': userprofile,
    }
    return render(request, 'accounts/edit_profile.html', context)

  def post(self, request, *args, **kwargs):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
          user_form.save()
          profile_form.save()
          messages.success(request, 'Your profile has been updated.')
          return redirect('edit_profile')
        else:
          messages.error(request, 'Error while updating Profile.')
          return redirect('edit_profile')

class UpdatePasswordView(View):
  @method_decorator(login_required(login_url='/accounts/login/'))
  def get(self, request, *args, **kwargs):
    return render(request, 'accounts/update_password.html')
  
  def post(self, request, *args, **kwargs):
    current_password = request.POST['current_password']
    new_password = request.POST['new_password']
    confirm_password = request.POST['confirm_password']

    user = Account.objects.get(username__exact=request.user.username)

    if new_password == confirm_password:
        success = user.check_password(current_password)
        if success:
            user.set_password(new_password)
            user.save()
            # auth.logout(request)
            messages.success(request, 'Password updated successfully.')
            return redirect('change_password')
        else:
            messages.error(request, 'Please enter valid current password')
            return redirect('change_password')
    else:
        messages.error(request, 'Password does not match!')
        return redirect('change_password')

class OrderDetailView(View):
  @method_decorator(login_required(login_url='/accounts/login/'))
  def get(self, request, order_id, *args, **kwargs):
    order_detail = OrderLine.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    subtotal = 0
    for i in order_detail:
        subtotal += i.product_price * i.quantity

    context = {
        'order_detail': order_detail,
        'order': order,
        'subtotal': subtotal,
    }
    return render(request, 'accounts/order_details.html', context)