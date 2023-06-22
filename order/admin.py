from django.contrib import admin
from .models import Payment, Order, OrderLine

class OrderProductInline(admin.TabularInline):
    model = OrderLine
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'payment_method', 'amount_paid', 'user', 'status')  
    list_filter = ('status',)
    search_fields = ('payment_id',)
    list_per_page = 25

    
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'payment', 'order_total', 'tax', 'status', 'is_ordered')  
    search_fields = ('order_number',)
    list_filter = ('status', 'is_ordered')
    list_per_page = 25
    inlines = [OrderProductInline]

    
class OrderLineAdmin(admin.ModelAdmin):
    list_display = ('order', 'product','quantity', 'product_price', 'ordered')  
    list_filter = ('ordered',)
    list_per_page = 25

# Register your models here.
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine, OrderLineAdmin)