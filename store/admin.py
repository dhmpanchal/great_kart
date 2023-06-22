from django.contrib import admin
from .models import Product, ProductVariation, ReviewRating, ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):

    list_display = ('image_tag', 'product_name', 'price', 'stock', 'category', 'created_at', 'is_active', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]
    list_filter = ('is_active','is_available', 'category')
    search_fields = ('product_name',)
    ordering = ('product_name',)
    readonly_fields = ('image_tag',)
    list_per_page = 10
    
    # def has_add_permission(self, request, obj=None):
    #     return True
    
    # def has_delete_permission(self, request, obj=None):
    #     return False


class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('variation_category', 'variation_value', 'product', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_active',)
    ordering = ('variation_category',)
    list_per_page = 10

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'subject', 'rating', 'status')
    list_filter = ('is_active', 'status')
    list_editable = ('status',)
    list_per_page = 10

class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ('product', 'image_tag')
    readonly_fields = ('image_tag',)
    list_per_page = 10

# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductVariation, ProductVariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery, ProductGalleryAdmin)