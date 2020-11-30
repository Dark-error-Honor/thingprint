from django.shortcuts import render, get_object_or_404, redirect
from django.views.defaults import page_not_found
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

import json
from .models import Thing, ThingUser, OrderItem, Order
from dashboard.extras import generate_order_id


def home_view(request):
    things = Thing.objects.all()

    context = {'things': things}

    return render(request, 'home/home.html', context)


def handler_404(request, exception):
    return page_not_found(request, exception, template_name='errors/404.html')


def detail_view(request, id):
    thing = Thing.objects.get(id=id)

    return render(request, 'products/detail_thing.html', {'thing': thing})


@login_required()
def add_to_cart(request, id):
    thing_user = get_object_or_404(ThingUser, user=request.user)
    thing = Thing.objects.get(id=id)

    order, created = Order.objects.get_or_create(
        owner=thing_user, is_ordered=False)
    if created:
        order.ref_code = generate_order_id()
        order.save()

    orderItem, item_created = OrderItem.objects.get_or_create(
        order=order, thing=thing)

    if not item_created:
        orderItem.quantity += 1
        orderItem.save
    else:
        orderItem.unique_key = generate_order_id()

    messages.info(request, 'Item added to cart')
    return redirect('/')


@login_required()
def delete_from_cart(request, id):
    thing = get_object_or_404(OrderItem, id=id)
    thing.delete()
    messages.info(request, 'Item removed from cart')
    return redirect('/cart')


@login_required()
def order_detail(request):
    order, created = Order.objects.get_or_create(
        owner=request.user.thinguser, is_ordered=False)
    if created:
        order.ref_code = generate_order_id()
        order.save()
    things = order.orderitem_set.all()
    context = {
        'things': things,
        'order': order,
    }
    return render(request, 'products/order_list.html', context)


@login_required()
def increment_quantity(request, id):
    thing = get_object_or_404(OrderItem, id=id)
    thing.quantity += 1
    thing.save()
    return redirect('/cart')


@login_required()
def decrement_quantity(request, id):
    thing = get_object_or_404(OrderItem, id=id)
    thing.quantity -= 1
    if thing.quantity <= 0:
        delete_from_cart(request, id)
        return redirect('/cart')
    thing.save()
    return redirect('/cart')


@login_required()
def payment_complete(request):
    body = json.loads(request.body)
    order = Order.objects.get(ref_code=body['code'])
    total = body['total']
    if float(order.get_cart_total) == float(total):
        order.is_ordered = True
        order.save()
        return redirect('/checkout/complete/{}'.format(order.ref_code))
    return redirect('/')


@login_required()
def checkout_view(request):
    order, created = Order.objects.get_or_create(
        owner=request.user.thinguser, is_ordered=False)
    if created:
        order.ref_code = generate_order_id()
        order.save()
    things = order.orderitem_set.all()
    context = {
        'things': things,
        'order': order,
    }
    return render(request, 'products/checkout.html', context)


@login_required()
def checkout_complete(request, ref_code):
    order = Order.objects.get(ref_code=ref_code)
    if order.is_ordered and order.owner == request.user.thinguser:
        context = {
            'order': order,
            'items': order.orderitem_set.all()
        }
    return render(request, 'products/success.html', context)
