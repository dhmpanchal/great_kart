from django.db import models
from django.urls import reverse
from accounts.models import Account
from category.models import Category
from extras.models import BaseModel
from django.utils.html import mark_safe
from django.db.models import Avg, Count

VARIATION_CATEGORY = [
    ('color', 'color'),
    ('size', 'size')
]

# Create your models here.
class Product(BaseModel):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "tbl_products"
        verbose_name = 'product'
        verbose_name_plural = 'products'
    
    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('products_detail', args=[self.category.slug, self.slug])
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def countReview(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count

    def image_tag(self):
        if self.images:
            return mark_safe('<img src="%s" width="70" height="70" />' % (self.images.url,))

    image_tag.short_description = 'Product Images'
    image_tag.allow_tags = True


class VariationManager(models.Manager):

    def colors(self):
        return super(VariationManager, self).filter(variation_category='color', is_active=True)
    
    def sizes(self):
        return super(VariationManager, self).filter(variation_category='size', is_active=True)


class ProductVariation(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=255, choices=VARIATION_CATEGORY)
    variation_value = models.CharField(max_length=255)

    objects = VariationManager()

    class Meta:
        db_table = "tbl_product_variation"
        verbose_name = 'product__variation'
        verbose_name_plural = 'product_variations'

    def __str__(self):
        if self.product:
            return self.product.product_name+":"+self.variation_value
        else:
            return 'Default Variant'


class ReviewRating(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = "tbl_review_rating"
        verbose_name = 'review_rating'
        verbose_name_plural = 'review_ratings'

    def __str__(self):
        if self.product:
            return f"{self.product.product_name} - {self.rating} - {self.subject}"
        else:
            return 'No Rating'


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    class Meta:
        db_table = "tbl_product_gallery"
        verbose_name = 'product_gallery'
        verbose_name_plural = 'product_galleries'

    def __str__(self):
        if self.product:
            return self.product.product_name
        return 'No Product'
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" width="70" height="70" />' % (self.image.url,))

    image_tag.short_description = 'Product Images'
    image_tag.allow_tags = True