from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from extras.utility import UtilityManager
from order.models import OrderLine
from store.forms import ReviewForm
from store.models import Product, ProductGallery, ReviewRating
from category.models import Category
from cart.models import ItemInCart
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.contrib import messages

# Create your views here.
class StoreView(View):

    def get(self, request, category_slug=None, *args, **kwargs):
        context = {}
        categories = None
        products = None

        if category_slug is not None:
            category = get_object_or_404(Category, slug=category_slug)
            products = Product.objects.filter(category=category,is_available=True).order_by('id')
        else:
            products = Product.objects.filter(is_available=True).order_by('id')

        paginator = Paginator(products, 6)
        page = request.GET.get('page')
        page_products = paginator.get_page(page)

        context = {
            'products': page_products,
            'total_products': products.count()
        }
        return render(request, 'thesite/store.html', context)

    
class ProductDetailView(View):
    
    def get(self, request, category_slug=None, product_slug=None, *args, **kwargs):
        context = {}
        
        try:
            product = Product.objects.get(category__slug=category_slug, slug=product_slug)
            the_utility = UtilityManager(request)
            in_cart = ItemInCart.objects.filter(cart__cart_id=the_utility.get_or_create_session()).exists()
        except Product.DoesNotExist as e:
            print(f"Product get failed==={e}")

        if request.user.is_authenticated:
            try:
                orderproduct = OrderLine.objects.filter(user=request.user, product_id=product.id).exists()
            except OrderLine.DoesNotExist:
                orderproduct = None
        else:
            orderproduct = None

        # Get the reviews
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

        # Get the product gallery
        product_gallery = ProductGallery.objects.filter(product_id=product.id)

        context = {
            'product': product,
            'in_cart': in_cart,
            'reviews': reviews,
            'product_gallery': product_gallery,
        }

        return render(request, 'thesite/product_detail.html', context)

class SearchView(View):

    def get(self, request, *args, **kwargs):
        if 'keyword' in request.GET:
            keyword = request.GET.get('keyword')
            products = Product.objects.filter(Q(product_name__icontains=keyword) or Q(description__icontains=keyword))
        context = {
            'products': products,
            'total_products': products.count()
        }
        return render(request, 'thesite/store.html', context) 


class ReviewsView(View):

    def post(self, request, product_id):
        url = request.META.get('HTTP_REFERER')
        if request.method == 'POST':
            try:
                reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
                form = ReviewForm(request.POST, instance=reviews)
                form.save()
                messages.success(request, 'Thank you! Your review has been updated.')
                return redirect(url)
            except ReviewRating.DoesNotExist:
                form = ReviewForm(request.POST)
                if form.is_valid():
                    data = ReviewRating()
                    data.subject = form.cleaned_data['subject']
                    data.rating = form.cleaned_data['rating']
                    data.review = form.cleaned_data['review']
                    data.ip = request.META.get('REMOTE_ADDR')
                    data.product_id = product_id
                    data.user_id = request.user.id
                    data.save()
                    messages.success(request, 'Thank you! Your review has been submitted.')
                    return redirect(url)