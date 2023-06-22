from django.urls import path
from .views import OrderCompleteView, OrderSummery, OrderView, PaymentView

urlpatterns = [
    path('place_order/', OrderView.as_view(), name="place_order"),
    path('order_summery/<order_number>/', OrderSummery.as_view(), name="order_summery"),
    path('payments/', PaymentView.as_view(), name='payments'),
    path('order_complete/', OrderCompleteView.as_view(), name='order_complete'),
]   