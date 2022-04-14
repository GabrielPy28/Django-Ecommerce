from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item/', views.UpdateItem, name='update'),
    path('process-order/', views.ProcessOrder, name='payment'),
]