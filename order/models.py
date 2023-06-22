from django.db import models
from extras.models import BaseModel
from accounts.models import Account
from store.models import Product, ProductVariation


# Create your models here.
class Payment(BaseModel):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='payment_account')
    payment_id = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=255, blank=True, null=True)
    amount_paid = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)


    class Meta:
        db_table = "tbl_payments"
        verbose_name = 'payment'
        verbose_name_plural = 'payments'

    def __str__(self):
        if self.payment_id != "":
            return self.payment_id
        return 'cod payment'


class Order(BaseModel):
    ORDER_STATUS = [
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='order_account', null=True, blank=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, related_name='order_account', null=True, blank=True)
    order_number = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address_line1 = models.CharField(max_length=255, blank=True, null=True)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    zip_code = models.CharField(max_length=255, blank=True, null=True)
    order_note = models.CharField(max_length=255, blank=True, null=True)
    order_total = models.FloatField(default=0.0)
    tax = models.FloatField(default=0.0)
    status = models.CharField(max_length=255,default=ORDER_STATUS[0][0], choices=ORDER_STATUS)
    ip = models.CharField(max_length=255, blank=True, null=True)
    is_ordered = models.BooleanField(default=False)


    class Meta:
        db_table = "tbl_orders"
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return self.order_number
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_address(self):
        return f"{self.address_line1} {self.address_line2}"


class OrderLine(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, related_name='payments_order_line', null=True, blank=True)
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, related_name='user_order_line', null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name='products_order_line', null=True, blank=True)
    variation = models.ManyToManyField(ProductVariation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)

    class Meta:
        db_table = "tbl_order_line"
        verbose_name = 'order_line'
        verbose_name_plural = 'order_lines'

    def __str__(self):
        if self.order:
            return self.order.order_number
        return 'Unknown order'
    
    @property
    def get_total_price(self):
        return self.product_price * self.quantity