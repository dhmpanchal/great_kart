from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ('image_tag', 'category_name', 'is_active', 'created_at')
    prepopulated_fields = {'slug': ('category_name',)}
    list_filter = ('is_active',)
    search_fields = ('category_name',)
    ordering = ('category_name',)
    readonly_fields = ('image_tag',)
    list_per_page = 10


# Register your models here.
admin.site.register(Category, CategoryAdmin)