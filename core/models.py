import os

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Thing(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.title


class ThingUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    owner = models.ForeignKey(ThingUser, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now=True)
    is_ordered = models.BooleanField(default=False)
    ref_code = models.CharField(max_length=20)

    @property
    def get_cart_total(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total for item in items])
        return total

    @property
    def get_cart_items(self):
        items = self.orderitem_set.all()
        total = sum([item.quantity for item in items])
        return total

    def __str__(self):
        return f'{self.owner} | {self.ref_code}'


class OrderItem(models.Model):
    thing = models.ForeignKey(Thing, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    date_added = models.DateTimeField(auto_now=True)
    unique_key = models.CharField(max_length=20)

    @property
    def get_total(self):
        return self.thing.price * self.quantity

    def __str__(self):
        return f'{self.thing.title} | {self.quantity}'


@receiver(models.signals.post_delete, sender=Thing)
def auto_delete_file_on_delete(sender, instance, **kwargs):

    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        ThingUser.objects.get_or_create(user=instance)


post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)
