from django.db import models
from store.models import Product, ProductVariation
from extras.models import BaseModel
from accounts.models import Account

# Create your models here.
class Cart(BaseModel):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "tbl_cart"
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def __str__(self):
        return self.cart_id

class ItemInCart(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(ProductVariation, blank=True)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    user    = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()

    class Meta:
        db_table = "tbl_item_in_cart"
        verbose_name = 'item_in_cart'
        verbose_name_plural = 'item_in_carts'

    def sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
