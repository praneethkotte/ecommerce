from django.urls import path

from . import views
from django.conf.urls import handler404, handler500

urlpatterns = [
        #Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	


]

# Custom error handlers

handler404 = 'store.views.error_404_view'
handler500 = 'store.views.error_500_view'