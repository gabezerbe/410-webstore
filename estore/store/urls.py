from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('store', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('product/<int:id>', views.product_details, name="product"),
    path('login', views.login_view, name="login"),
    path('register', views.register_view, name="register"),
    path('logout', views.logout_view, name="logout"),
    
    path('update_item/', views.update_item, name="update_item"),
    path('processOrder/', views.processOrder, name="processOrder"),

]