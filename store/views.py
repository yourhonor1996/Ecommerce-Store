import json
from store.models import Customer, OrderItem, Product, Order
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
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print({'Action:':action, 'ProductId:':productId})
        
        customer = request.user.customer
        product = Product.objects.get(id= productId)
        order, created = Order.objects.get_or_create(customer= customer, complete= False)
        order_item, created = OrderItem.objects.get_or_create(order= order, product= product)
        
        if action == 'add':
            order_item.quantity += 1
        elif action == 'remove':
            order_item.quantity -= 1
        
        order_item.save()
        
        if order_item.quantity <= 0:
            order_item.delete()
        return JsonResponse('Item was added', safe= False)