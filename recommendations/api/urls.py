from django.urls import path
from .views import top_buys, bought_together

urlpatterns = [
    path("top-buys/", top_buys),
    path("bought-together/<int:product_id>/", bought_together),
]
