from django.urls import path
from .views import ReviewsView, SearchView, StoreView, ProductDetailView

urlpatterns = [
    path('', StoreView.as_view(), name="store"),
    path('category/<slug:category_slug>/', StoreView.as_view(), name="products_by_cats"),
    path('category/<slug:category_slug>/<slug:product_slug>/', ProductDetailView.as_view(), name="products_detail"),
    path('search/', SearchView.as_view(), name="search"),
    path('reviews/<int:product_id>/', ReviewsView.as_view(), name="reviews"),
]