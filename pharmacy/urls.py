from django.contrib import admin
from django.urls import path
from pharmacy import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('search/', views.search, name='search'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('upload_prescription/', views.upload_prescription, name='upload_prescription'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)