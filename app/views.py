import json
import logging

from .models import *

from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

_logger = logging.Logger('__name__')


def register(request):
    if request.user.is_authenticated:
        user_login = 'show'
        user_not_login = 'hidden'
    else:
        user_login = 'hidden'
        user_not_login = 'show'
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(to='login')
    context = {'form': form, 'user_login': user_login, 'user_not_login': user_not_login}
    return render(request, template_name='app/register.html', context=context)

def loginPage(request):
    if request.user.is_authenticated:
        user_login = 'show'
        user_not_login = 'hidden'
        return redirect('home')
    else:
        user_login = 'hidden'
        user_not_login = 'show'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(to='home')
        else:
            messages.info(request=request, message='Login failed')
    context = {
        'user_login': user_login,
        'user_not_login': user_not_login
    }
    return render(request, template_name='app/login.html', context=context)


@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    storage = messages.get_messages(request)
    storage.used = True
    messages.add_message(request, messages.SUCCESS, "Sign in again")
    return redirect(to='login')


def home(request):
    products = Product.objects.all()
    # products = Product.objects.filter()
    total_order_items = 0
    if request.user.is_authenticated:
        customer = request.user
        order_items, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_order_items = order_items.get_total_order_item_quantity
        user_login = 'show'
        user_not_login = 'hidden'
    else:
        user_login = 'hidden'
        user_not_login = 'show'

    context = {
        'products': products,
        'nav': 'home',
        'total_order_items': total_order_items,
        'user_login': user_login,
        'user_not_login': user_not_login,
        'categories': Category.objects.filter(is_sub=False)
    }
    return render(request, template_name='app/home.html', context=context)


def search(request):
    try:
        if request.method == 'POST':
            searched = request.POST.get('searched')
            if not searched:
                return redirect(to='home')
            keys = Product.objects.filter(name__contains=searched)

        total_order_items = 0
        if request.user.is_authenticated:
            customer = request.user
            order_items, created = Order.objects.get_or_create(customer=customer, complete=False)
            total_order_items = order_items.get_total_order_item_quantity
            user_login = 'show'
            user_not_login = 'hidden'
        else:
            user_login = 'hidden'
            user_not_login = 'show'

        context = {
            'searched': searched,
            'keys': keys,
            'total_order_items': total_order_items,
            'user_login': user_login,
            'user_not_login': user_not_login,
            'categories': Category.objects.filter(is_sub=False)
        }
        return render(request, template_name='app/search.html', context=context)
    except Exception as e:
        _logger.error(e, exc_info=True)
        return redirect(to='home')


def category(request):
    categories = Category.objects.filter(is_sub=False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context = {
        'categories': categories,
        'active_category': active_category,
        'products': products,
    }
    return render(request, template_name='app/category.html', context=context)

def detail(request):
    total_order_items = 0
    if request.user.is_authenticated:
        customer = request.user
        order_items, created = Order.objects.get_or_create(customer=customer, complete=False)
        total_order_items = order_items.get_total_order_item_quantity
        user_login = 'show'
        user_not_login = 'hidden'
    else:
        user_login = 'hidden'
        user_not_login = 'show'

    id = request.GET.get('id')
    product = Product.objects.filter(id=id)

    context = {
        'product': product[0],
        'total_order_items': total_order_items,
        'user_login': user_login,
        'user_not_login': user_not_login,
        'categories': Category.objects.filter(is_sub=False)
    }
    return render(request, template_name='app/detail.html', context=context)


def cart(request):
    try:
        total_order_items = 0
        order = None
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            # order = Order.objects.get(customer=customer, complete=False)
            order_items = order.orderitem_set.all()
            total_order_items = order.get_total_order_item_quantity
            user_login = 'show'
            user_not_login = 'hidden'
        else:
            order_items = []
            user_login = 'hidden'
            user_not_login = 'show'

        context = {
            'order': order,
            'order_items': order_items,
            'nav': 'cart',
            'total_order_items': total_order_items,
            'user_login': user_login,
            'user_not_login': user_not_login,
            'categories': Category.objects.filter(is_sub=False)
        }
    except Exception as e:
        _logger.error(e)
        return render(request, 'app/cart.html')

    return render(request, 'app/cart.html', context)


def checkout(request):
    context = {}
    try:
        order = None
        order_items = None
        total_order_items = 0
        if request.user.is_authenticated:
            customer = request.user
            order = Order.objects.get(customer=customer, complete=False)
            order_items = order.orderitem_set.all()
            total_order_items = order.get_total_order_item_quantity
            user_login = 'show'
            user_not_login = 'hidden'
        else:
            user_login = 'hidden'
            user_not_login = 'show'

        context.update({
            'order': order,
            'order_items': order_items,
            'total_order_items': total_order_items,
            'user_login': user_login,
            'user_not_login': user_not_login,
            'categories': Category.objects.filter(is_sub=False)
        })
    except Exception as e:
        _logger.error(str(e))

    return render(request, template_name='app/checkout.html', context=context)


def about_us(request):
    user = ''
    if request.user.is_authenticated:
        user = request.user
        # print(user)
        user_login = 'show'
        user_not_login = 'hidden'
    else:
        user_login = 'hidden'
        user_not_login = 'show'
    context = {
        'user': user,
        'user_login': user_login,
        'user_not_login': user_not_login
    }
    return render(request, 'app/about_us.html', context=context)


def update_item(request):
    data = json.loads(request.body)
    # print(data)
    product_id = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()
    return JsonResponse('added', safe=False)


def input_shipping_info(request):
    if request.method == 'POST':
        req = request.POST
        name = req.get('name', '')
        email = req.get('email', '')
        mobile = req.get('mobile', '')
        address = req.get('address', '')
        city = req.get('city', '')

    if request.user.is_authenticated:
        customer = request.user
        order, order_created = Order.objects.get_or_create(customer=customer, complete=False)
        shipping_address, shipping_address_created = ShippingAddress.objects.get_or_create(customer=customer, order=order)
        if order.orderitem_set.all():
            shipping_address.name = name
            shipping_address.email = email
            shipping_address.mobile = mobile
            shipping_address.address = address
            shipping_address.city = city
            shipping_address.save()

            order.complete = True
            order.save()
        else:
            print('chua co gi de ma checkout')
            return HttpResponse('chua co gi de ma checkout')
    return redirect(to='home')
