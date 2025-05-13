from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Medicine, Cart, Prescription, Order, OrderItem
from .forms import SignUpForm, PrescriptionForm
from django.http import JsonResponse
from django.db.models import Q
def home(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def search(request):
    query = request.GET.get('q', '')
    medicines = Medicine.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        results = [{'id': m.id, 'name': m.name, 'price': str(m.price), 'image': m.image} for m in medicines]
        return JsonResponse({'results': results})
    return render(request, 'search.html', {'medicines': medicines, 'query': query})

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.medicine.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def add_to_cart(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, medicine=medicine)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('cart')

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    return redirect('cart')

@login_required
def upload_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.user = request.user
            prescription.save()
            messages.success(request, 'Prescription uploaded successfully!')
            return redirect('checkout')
    else:
        form = PrescriptionForm()
    return render(request, 'upload_prescription.html', {'form': form})

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.medicine.price * item.quantity for item in cart_items)
    prescription = Prescription.objects.filter(user=request.user).last()
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, prescription=prescription)
        for item in cart_items:
            OrderItem.objects.create(order=order, medicine=item.medicine, quantity=item.quantity)
        cart_items.delete()
        return redirect('order_confirmation', order_id=order.id)
    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total, 'prescription': prescription})

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})