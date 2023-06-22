from django.db import models
from extras.models import BaseModel
from django.utils.html import mark_safe
from django.urls import reverse

# Create your models here.
class Category(BaseModel):
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to='photos/categories')

    class Meta:
        db_table = "tbl_categories"
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    
    def get_url(self):
        return reverse('products_by_cats', args=[self.slug])

    def __str__(self):
        return self.category_name

    def image_tag(self):
        if self.cat_image:
            return mark_safe('<img src="%s" width="70" height="70" />' % (self.cat_image.url,))

    image_tag.short_description = 'Category Image'
    image_tag.allow_tags = True
