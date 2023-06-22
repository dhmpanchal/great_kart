from django.shortcuts import render
from django.views import View
from store.models import Product, ReviewRating

# Create your views here.
class SiteBaseView(View):

    def get(self, request, *args, **kwargs):
        context = {}

        products = Product.objects.filter(is_available=True)

        # Get the reviews
        reviews = None
        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id, status=True)


        context = {
            'products': products,
            'reviews': reviews,
        }
        return render(request, 'thesite/index.html', context)