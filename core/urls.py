from django.urls import path
from .views import home_view, detail_view, add_to_cart, delete_from_cart, order_detail, increment_quantity, decrement_quantity, payment_complete, checkout_view, checkout_complete

urlpatterns = [
    path('', home_view),
    path('thing/<int:id>', detail_view),
    path('add-cart/<int:id>', add_to_cart),
    path('del-cart/<int:id>', delete_from_cart),
    path('cart', order_detail),
    path('increment/<int:id>', increment_quantity),
    path('decrement/<int:id>', decrement_quantity),
    path('set-value/<int:id>/<int:quantity>', decrement_quantity),
    path('checkout/complete/<int:ref_code>',
         checkout_complete, name="checkout-complete"),
    path('checkout/', checkout_view, name="checkout"),
    path('purchase-complete/', payment_complete, name="order-complete"),
]
