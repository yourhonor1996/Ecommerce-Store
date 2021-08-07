from store.models import Customer, Product, Order
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse

class CartView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer= customer, complete= False)
            items = order.orderitem_set.all()
        else:
            # If the user is not authenticated, then just return an empty order.
            items = Order.objects.none() 
            order = Order()
        
        context = {'items':items, 'order': order}
        return render(request, 'store/cart.html', context)
    
class StoreView(View):
    
    def get(self, request):
        products = Product.objects.all()
    
        context = {'products':products}
        return render(request, 'store/store.html', context)

class CheckoutView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer= customer, complete= False)
            items = order.orderitem_set.all()
        else:
            # If the user is not authenticated, then just return an empty order.
            items = Order.objects.none() 
            order = Order()
        
        context = {'items':items, 'order': order}
        return render(request, 'store/checkout.html', context)

class UpdateItemView(View):
    
    def post(self, request):
        return JsonResponse('Item was added', safe= False)