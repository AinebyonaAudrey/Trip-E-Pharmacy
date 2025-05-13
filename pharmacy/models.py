from django.db import models
from django.contrib.auth.models import User

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=200)  # Stores image URL

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.medicine.name}"

class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='prescriptions/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription for {self.user.username}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicines = models.ManyToManyField(Medicine, through='OrderItem')
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.medicine.name} in Order {self.order.id}"