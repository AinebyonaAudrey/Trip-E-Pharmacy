from django.contrib import admin
from .models import Medicine, Cart, Prescription, Order, OrderItem

admin.site.register(Medicine)
admin.site.register(Cart)
admin.site.register(Prescription)
admin.site.register(Order)
admin.site.register(OrderItem)