from store.models import Customer, Product, Order
from django.shortcuts import render
from django.views import View


class CartView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer= customer, complete= False)
            items = order.orderitem_set.all()
        else:
            items = []
            order = {'get_cart_total':0, 'get_cart_items_count':0}
        
        context = {'items':items, 'order': order}
        return render(request, 'store/cart.html', context)
    
class StoreView(View):
    
    def get(self, request):
        products = Product.objects.all()
    
        context = {'products':products}
        return render(request, 'store/store.html', context)

class CheckoutView(View):
    
    def get(self, request):
        context = {}
        return render(request, 'store/checkout.html', context)

