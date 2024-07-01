from django.urls import path,include
from core import views

urlpatterns = [
    path('',views.index,name='index'),
    path('add_product',views.add_product,name="add_product"),

    path('product_disc/<int:pk>',views.product_disc,name="product_disc"),
    path('add_to_cart/<int:pk>',views.add_to_cart,name="add_to_cart"),
    # path('add_to_cart/<int:pk>', views.add_to_cart, name="add_to_cart"),
    path('orderlist',views.orderlist,name="orderlist"),
    path('add_item/<int:pk>',views.add_item,name="add_item"),
    path('remove_item/<int:pk>',views.remove_item,name="remove_item"),
    path('checkout_page',views.checkout_page,name="checkout_page"),
    path('payment',views.payment,name="payment"),
    path('payment_success/',views.payment_success, name='payment_success'),
    path('order_history/', views.order_history, name='order_history'),
    path('delete_item/<int:pk>/', views.delete_item, name='delete_item'),  

]
