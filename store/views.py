import json
from store.models import Customer, OrderItem, Product, Order, ShippingAddress
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from datetime import datetime

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
        productId = data.get('productId')
        action = data.get('action')
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
        return JsonResponse({'cart_item_count': order.get_cart_items_count}, safe= False)


class InfoAPIView(View):
    # permission_classes = (IsAuthenticated, )

    def get(self, request):
        # product = Product.objects.get(id= productId)
        # order_item, created = OrderItem.objects.get_or_create(order= order, product= product)
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer= customer, complete= False)
            return JsonResponse(data={'cart_item_count':order.get_cart_items_count}) 
        else:
            return JsonResponse(data={'cart_item_count':0}) 
        # order_item.save()
        # if order_item.quantity <= 0:
        #     order_item.delete()
        # return JsonResponse({'cart_item_count': order.get_cart_items_count}, safe= False)


class ProcessOrderView(View):
    
    def post(self, request):
        transacion_id = datetime.now().timestamp()
        data = json.loads(request.body)
        
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer= customer, complete= False)
            form = data['form']
            total = float(form['total'])
            order.transaction_id = transacion_id
            
            if total == order.get_cart_total:
                order.complete = True
            order.save()

            if order.shipping == True:
                ShippingAddress.objects.create(
                    customer= customer,
                    order= order,
                    address = form['address'],
                    city= form['city'],
                    zipcode= form['zipcode'] 

                )
            
        else:
            print('user is not logged in')

        return JsonResponse('Payment Complete!', safe= False)