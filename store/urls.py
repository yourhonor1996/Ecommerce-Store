from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.store, name= 'store'),
    path('cart/', views.cart, name= 'cart'),
    path('checkout/', views.checkout, name= 'checkout')
]


