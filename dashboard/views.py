from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Thing, ThingUser, OrderItem, Order
from core.forms import ThingForm
from dashboard.extras import generate_order_id

from django.contrib.auth.decorators import login_required
# Create your views here.


def main_dashboard_view(request):
    return render(request, 'dashboard/dashboard.html', {})


def create_thing_view(request):
    if request.method == 'POST':
        form = ThingForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form = ThingForm()
    else:
        form = ThingForm()
    return render(request, 'products/create_thing.html', {'form': form})


def manage_things_view(request):
    if request.method == 'POST':
        print(request.POST)
    things = Thing.objects.all()
    return render(request, 'dashboard/manage.html', {'things': things})


def remove_thing_view(request, id):
    if request.user.is_superuser:
        obj = Thing.objects.get(id=id)
        obj.delete()
        return redirect('/dashboard/manage')
    else:
        return redirect('/')


def edit_thing_view(request, id):
    thing = Thing.objects.get(pk=id)
    if request.method == 'POST':
        form = ThingForm(request.POST, request.FILES, instance=thing)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/manage')
    else:
        form = ThingForm(instance=thing)
    return render(request, 'products/edit_thing.html', {'form': form})
