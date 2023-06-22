from django.urls import path
from .views import SiteBaseView

urlpatterns = [
    path('', SiteBaseView.as_view(), name="site-index-view"),
]