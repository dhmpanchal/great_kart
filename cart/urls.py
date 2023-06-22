from django.urls import path
from .views import CartView, AddCartView, CheckoutView, RemoveCartView, RemoveCartItemView

urlpatterns = [
    path('', CartView.as_view(), name="cart_view"),
    path('add_cart/<int:product_id>/', AddCartView.as_view(), name="add_cart"),
    path('remove_cart/<int:product_id>/<int:cart_item_id>/', RemoveCartView.as_view(), name="remove_cart"),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', RemoveCartItemView.as_view(), name="remove_cart_item"),

    path('checkout/', CheckoutView.as_view(), name="checkout_view"),
]