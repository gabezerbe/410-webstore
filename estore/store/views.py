from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import *
from django.contrib.auth import *
from django.http import JsonResponse
import json
import datetime
# Create your views here.

def store(request):
    products = Product.objects.all()
    context = {'products':products}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
    context = {'items':items, 'order':order, 'shipping':False}
    return render(request, 'store/checkout.html', context)

def product_details(request, id):
    product = Product.objects.get(product_id = id)
    context = {'product' : product}
    return render(request, 'store/product.html', context)

def register_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('store')
    else:
        form=UserCreationForm()

    context = {'form':form}
    return render(request, 'store/register.html', context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('store')
    else:
        if request.method =='POST':
            #dummy value to avoid an intendation error
            form = AuthenticationForm(data = request.POST)
            if form.is_valid():
                #retrieve user
                user = form.get_user()
                #log that user in
                login(request, user)
                return redirect('store')
        else:
            form = AuthenticationForm()

        context = {'form':form}
        return render(request, 'store/login.html', context)

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

def update_item(request):
    data = json.loads(request.body)
    productID = data['productID']
    action= data['action']
    print('Action:', action)
    print('Product:', productID)

    customer = request.user.customer
    product = Product.objects.get(product_id=productID)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was updated...", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zip_code=data['shipping']['zipcode'],
        )

    else:
        print("User is not logged in")
    return JsonResponse('Payment Complete...', safe = False)