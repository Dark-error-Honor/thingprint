from django.contrib import admin
from .models import Thing, ThingUser, OrderItem, Order

# Register your models here.
admin.site.register(Thing)
admin.site.register(ThingUser)
admin.site.register(OrderItem)
admin.site.register(Order)
